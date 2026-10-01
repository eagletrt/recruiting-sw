"""Vehicle-side CAN gateway (plays the role of the car's control unit).

CAN -> sim: decodes AS_CMD and forwards it to /sim/actuator_cmd.
sim -> CAN: encodes the vehicle speed into VEH_SPEED.
If AS_CMD stops arriving for longer than cmd_timeout, the emergency brake
engages and stays on until /can_gateway/reset is called.
"""
import os
import random

import can
import cantools
import rclpy
from ament_index_python.packages import get_package_share_directory
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_srvs.srv import Trigger

from eagle_msgs.msg import ActuatorCmd, GatewayStatus


class CanGateway(Node):
    def __init__(self):
        super().__init__('can_gateway')
        p = self.declare_parameter
        default_dbc = os.path.join(get_package_share_directory('eagle_sim'), 'can', 'eagle_task.dbc')
        self.db = cantools.database.load_file(p('dbc_path', default_dbc).value)
        interface = p('can_interface', 'socketcan').value
        channel = p('can_channel', 'vcan0').value
        self.cmd_timeout = p('cmd_timeout', 0.2).value
        self.speed_noise = p('speed_noise_std', 0.0).value

        self.bus = can.Bus(interface=interface, channel=channel)
        self.get_logger().info(f'CAN bus: {interface}/{channel}')
        self.reset()

        self.cmd_pub = self.create_publisher(ActuatorCmd, '/sim/actuator_cmd', 10)
        self.status_pub = self.create_publisher(GatewayStatus, '/sim/gateway_status', 10)
        self.create_subscription(Odometry, '/sim/ground_truth/odom', self.on_odom, 10)
        self.create_service(Trigger, '/can_gateway/reset', self.on_reset)
        self.create_timer(0.005, self.read_can)
        self.create_timer(0.01, self.publish_cmd)

    def reset(self):
        self.throttle = 0.0
        self.brake = 0.0
        self.mission_finished = False
        self.emergency_brake = False
        self.last_cmd_time = None

    def on_reset(self, _request, response):
        self.reset()
        self.get_logger().info('Gateway reset')
        response.success = True
        return response

    def read_can(self):
        """Receive every AS_CMD frame waiting on the bus."""
        while (frame := self.bus.recv(timeout=0.0)) is not None:
            if frame.arbitration_id != self.db.get_message_by_name('AS_CMD').frame_id:
                continue
            try:
                signals = self.db.decode_message('AS_CMD', frame.data)
            except Exception as e:  # malformed frame
                self.get_logger().warn(f'Cannot decode AS_CMD {frame.data.hex()}: {e}', throttle_duration_sec=1.0)
                continue
            self.throttle = min(max(signals['ThrottleReq'], 0.0), 1.0)
            self.brake = min(max(signals['BrakeReq'], 0.0), 1.0)
            self.mission_finished = bool(signals['MissionFinished'])
            self.last_cmd_time = self.get_clock().now()

    def publish_cmd(self):
        now = self.get_clock().now()
        if self.last_cmd_time is not None and not self.emergency_brake:
            silence = (now - self.last_cmd_time).nanoseconds * 1e-9
            if silence > self.cmd_timeout:
                self.emergency_brake = True
                self.get_logger().error(f'EMERGENCY BRAKE: no AS_CMD for {silence * 1000:.0f} ms')

        cmd = ActuatorCmd()
        cmd.header.stamp = now.to_msg()
        cmd.emergency_brake = self.emergency_brake
        cmd.throttle = 0.0 if self.mission_finished else self.throttle
        cmd.brake = 1.0 if self.mission_finished else self.brake
        self.cmd_pub.publish(cmd)

        status = GatewayStatus()
        status.header.stamp = cmd.header.stamp
        status.emergency_brake = self.emergency_brake
        status.mission_finished = self.mission_finished
        status.throttle_request = self.throttle
        status.brake_request = self.brake
        self.status_pub.publish(status)

    def on_odom(self, msg: Odometry):
        speed = msg.twist.twist.linear.x
        if self.speed_noise > 0.0:
            speed += random.gauss(0.0, self.speed_noise)
        data = self.db.encode_message('VEH_SPEED', {'VehicleSpeed': min(max(speed, 0.0), 40.0)})
        frame_id = self.db.get_message_by_name('VEH_SPEED').frame_id
        try:
            self.bus.send(can.Message(arbitration_id=frame_id, data=data, is_extended_id=False))
        except can.CanError as e:
            self.get_logger().warn(f'CAN send failed: {e}', throttle_duration_sec=2.0)

    def destroy_node(self):
        self.bus.shutdown()
        super().destroy_node()


def main():
    rclpy.init()
    node = CanGateway()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
