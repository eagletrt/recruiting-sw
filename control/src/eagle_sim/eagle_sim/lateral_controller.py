"""Pure-pursuit lateral controller following the candidate's centerline.

Subscribes to /planning/centerline (nav_msgs/Path, any frame with a TF to
base_link). If the path is missing or stale the steering is held at zero.
"""
import math

import rclpy
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import Float64
from tf2_ros import Buffer, TransformException, TransformListener

from eagle_sim.fake_perception import yaw_from_quaternion


class LateralController(Node):
    def __init__(self):
        super().__init__('lateral_controller')
        p = self.declare_parameter
        self.wheelbase = p('wheelbase', 1.53).value
        self.min_lookahead = p('min_lookahead', 3.0).value
        self.lookahead_gain = p('lookahead_gain', 0.3).value
        self.path_timeout = p('path_timeout', 0.5).value
        self.base_frame = p('base_frame', 'base_link').value
        rate = p('rate', 50.0).value

        self.path = None
        self.path_time = None
        self.speed = 0.0

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_subscription(Path, '/planning/centerline', self.on_path, 10)
        self.create_subscription(Odometry, '/sim/ground_truth/odom', self.on_odom, 10)
        self.steer_pub = self.create_publisher(Float64, '/sim/steering_cmd', 10)
        self.create_timer(1.0 / rate, self.on_timer)

    def on_path(self, msg: Path):
        self.path = msg
        self.path_time = self.get_clock().now()

    def on_odom(self, msg: Odometry):
        self.speed = msg.twist.twist.linear.x

    def path_in_base(self):
        """Path points in base_link, or None if unavailable."""
        if self.path is None or not self.path.poses:
            return None
        if (self.get_clock().now() - self.path_time).nanoseconds * 1e-9 > self.path_timeout:
            self.get_logger().warn('Centerline is stale, holding steering straight', throttle_duration_sec=2.0)
            return None
        frame = self.path.header.frame_id or self.base_frame
        try:
            tf = self.tf_buffer.lookup_transform(self.base_frame, frame, Time())
        except TransformException as e:
            self.get_logger().warn(f'Cannot transform centerline: {e}', throttle_duration_sec=2.0)
            return None
        yaw = yaw_from_quaternion(tf.transform.rotation)
        c, s = math.cos(yaw), math.sin(yaw)
        tx, ty = tf.transform.translation.x, tf.transform.translation.y
        return [(c * ps.pose.position.x - s * ps.pose.position.y + tx,
                 s * ps.pose.position.x + c * ps.pose.position.y + ty) for ps in self.path.poses]

    def on_timer(self):
        points = self.path_in_base()
        steer = 0.0
        if points:
            lookahead = max(self.min_lookahead, self.lookahead_gain * self.speed)
            ahead = [pt for pt in points if pt[0] > 0.0]
            target = next((pt for pt in ahead if math.hypot(*pt) >= lookahead), ahead[-1] if ahead else None)
            if target is not None:
                dist = math.hypot(*target)
                alpha = math.atan2(target[1], target[0])
                steer = math.atan2(2.0 * self.wheelbase * math.sin(alpha), dist)
        self.steer_pub.publish(Float64(data=steer))


def main():
    rclpy.init()
    node = LateralController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
