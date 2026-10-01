"""Vehicle simulation: kinematic bicycle with longitudinal dynamics.

base_link sits on the rear axle centre. Actuators have first-order lag.
Inputs come only from can_gateway (/sim/actuator_cmd) and lateral_controller
(/sim/steering_cmd); if actuator commands go stale the emergency brake engages.
"""
import math
from dataclasses import dataclass

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Float64
from std_srvs.srv import Trigger
from tf2_ros import TransformBroadcaster
from visualization_msgs.msg import Marker, MarkerArray

from eagle_msgs.msg import ActuatorCmd

G = 9.81
AIR_DENSITY = 1.2


@dataclass
class State:
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0
    v: float = 0.0
    throttle: float = 0.0
    brake: float = 0.0
    steer: float = 0.0


class VehicleSim(Node):
    def __init__(self):
        super().__init__('vehicle_sim')
        p = self.declare_parameter
        self.mass = p('mass', 250.0).value
        self.wheelbase = p('wheelbase', 1.53).value
        self.track = p('track_width', 1.2).value
        self.wheel_radius = p('wheel_radius', 0.2).value
        self.max_drive_force = p('max_drive_force', 2000.0).value
        self.max_power = p('max_power', 40000.0).value
        self.max_brake_force = p('max_brake_force', 3200.0).value
        self.ebs_brake_force = p('ebs_brake_force', 2500.0).value
        self.cda = p('cda', 1.2).value
        self.rolling_coeff = p('rolling_coeff', 0.015).value
        self.tau_throttle = p('tau_throttle', 0.08).value
        self.tau_brake = p('tau_brake', 0.05).value
        self.tau_steer = p('tau_steer', 0.1).value
        self.max_steer = p('max_steer', 0.4).value
        self.cmd_timeout = p('cmd_timeout', 0.2).value
        self.init_x = p('initial_x', 0.0).value
        self.init_y = p('initial_y', 0.0).value
        self.init_yaw = p('initial_yaw', 0.0).value
        self.map_frame = p('map_frame', 'map').value
        self.base_frame = p('base_frame', 'base_link').value
        self.sim_dt = p('sim_dt', 0.001).value
        publish_rate = p('publish_rate', 100.0).value

        self.state = State()
        self.reset()

        self.cmd = ActuatorCmd()
        self.cmd_time = None
        self.steer_cmd = 0.0
        self.ebs_latched = False

        self.tf_broadcaster = TransformBroadcaster(self)
        self.odom_pub = self.create_publisher(Odometry, '/sim/ground_truth/odom', 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/sim/vehicle_markers', 1)
        self.create_subscription(ActuatorCmd, '/sim/actuator_cmd', self.on_cmd, 10)
        self.create_subscription(Float64, '/sim/steering_cmd', self.on_steer, 10)
        self.create_service(Trigger, '/sim/reset', self.on_reset)

        self.last_step = self.get_clock().now()
        self.create_timer(1.0 / publish_rate, self.on_timer)
        self.create_timer(1.0, self.publish_markers)

    def reset(self):
        self.state = State(x=self.init_x, y=self.init_y, yaw=self.init_yaw)
        self.ebs_latched = False

    def on_cmd(self, msg: ActuatorCmd):
        self.cmd = msg
        self.cmd_time = self.get_clock().now()

    def on_steer(self, msg: Float64):
        self.steer_cmd = max(-self.max_steer, min(self.max_steer, msg.data))

    def on_reset(self, _request, response):
        self.reset()
        self.cmd = ActuatorCmd()
        self.cmd_time = None
        self.steer_cmd = 0.0
        response.success = True
        return response

    def emergency_active(self, now) -> bool:
        stale = self.cmd_time is not None and \
            (now - self.cmd_time).nanoseconds * 1e-9 > self.cmd_timeout
        if self.cmd.emergency_brake or stale:
            if not self.ebs_latched:
                self.get_logger().warn('Emergency brake engaged' + (' (command timeout)' if stale else ''))
            self.ebs_latched = True
        return self.ebs_latched

    def step(self, dt: float, ebs: bool):
        s = self.state
        throttle_target = 0.0 if ebs else min(max(self.cmd.throttle, 0.0), 1.0)
        brake_target = 0.0 if ebs else min(max(self.cmd.brake, 0.0), 1.0)
        s.throttle += (throttle_target - s.throttle) * min(dt / self.tau_throttle, 1.0)
        s.brake += (brake_target - s.brake) * min(dt / self.tau_brake, 1.0)
        s.steer += (self.steer_cmd - s.steer) * min(dt / self.tau_steer, 1.0)

        drive = s.throttle * min(self.max_drive_force, self.max_power / max(s.v, 0.1))
        brake = self.ebs_brake_force if ebs else s.brake * self.max_brake_force
        resist = 0.5 * AIR_DENSITY * self.cda * s.v ** 2 + self.rolling_coeff * self.mass * G
        if s.v <= 0.0:
            brake = 0.0
            resist = 0.0
        s.v = max(0.0, s.v + (drive - brake - resist) / self.mass * dt)

        s.x += s.v * math.cos(s.yaw) * dt
        s.y += s.v * math.sin(s.yaw) * dt
        s.yaw += s.v / self.wheelbase * math.tan(s.steer) * dt

    def on_timer(self):
        now = self.get_clock().now()
        elapsed = (now - self.last_step).nanoseconds * 1e-9
        self.last_step = now
        ebs = self.emergency_active(now)
        steps = max(1, round(elapsed / self.sim_dt))
        for _ in range(steps):
            self.step(elapsed / steps, ebs)
        self.publish_state(now)

    def publish_state(self, now):
        s = self.state
        stamp = now.to_msg()
        qz, qw = math.sin(s.yaw / 2.0), math.cos(s.yaw / 2.0)
        yaw_rate = s.v / self.wheelbase * math.tan(s.steer)

        tf = TransformStamped()
        tf.header.stamp = stamp
        tf.header.frame_id = self.map_frame
        tf.child_frame_id = self.base_frame
        tf.transform.translation.x = s.x
        tf.transform.translation.y = s.y
        tf.transform.rotation.z = qz
        tf.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(tf)

        odom = Odometry()
        odom.header = tf.header
        odom.child_frame_id = self.base_frame
        odom.pose.pose.position.x = s.x
        odom.pose.pose.position.y = s.y
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw
        odom.twist.twist.linear.x = s.v
        odom.twist.twist.angular.z = yaw_rate
        self.odom_pub.publish(odom)

    def publish_markers(self):
        def marker(marker_id, marker_type, pos, scale, rgba, rot_x=False):
            m = Marker()
            m.header.frame_id = self.base_frame
            m.ns = 'vehicle'
            m.id = marker_id
            m.type = marker_type
            m.frame_locked = True
            m.pose.position.x, m.pose.position.y, m.pose.position.z = pos
            if rot_x:  # cylinder axis along y for wheels
                m.pose.orientation.x = math.sin(math.pi / 4.0)
                m.pose.orientation.w = math.cos(math.pi / 4.0)
            else:
                m.pose.orientation.w = 1.0
            m.scale.x, m.scale.y, m.scale.z = scale
            m.color.r, m.color.g, m.color.b, m.color.a = rgba
            return m

        r = self.wheel_radius
        body = (0.85, 0.1, 0.1, 1.0)
        wheel = (0.08, 0.08, 0.08, 1.0)
        half = self.track / 2.0
        markers = MarkerArray()
        markers.markers = [
            marker(0, Marker.CUBE, (self.wheelbase / 2.0, 0.0, r + 0.05), (2.4, 0.5, 0.3), body),
            marker(1, Marker.CUBE, (self.wheelbase + 0.75, 0.0, r), (0.3, 1.2, 0.05), body),  # front wing
            marker(2, Marker.CUBE, (-0.45, 0.0, r + 0.7), (0.3, 1.0, 0.05), body),  # rear wing
            marker(3, Marker.CUBE, (0.4, 0.0, r + 0.35), (0.25, 0.15, 0.4), (0.1, 0.1, 0.1, 1.0)),  # main hoop
        ]
        for i, (x, y) in enumerate(((0.0, half), (0.0, -half),
                                    (self.wheelbase, half), (self.wheelbase, -half))):
            markers.markers.append(marker(10 + i, Marker.CYLINDER, (x, y, r), (2 * r, 2 * r, 0.2), wheel, rot_x=True))
        self.marker_pub.publish(markers)


def main():
    rclpy.init()
    node = VehicleSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
