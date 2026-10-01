"""Publishes the track cones visible from the current vehicle pose.

Cones are expressed in the vehicle frame, limited by range and field of view,
optionally noisy / dropped, and sorted by ascending distance.
"""
import math
import random

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener

from eagle_msgs.msg import Cone, ConeArray
from eagle_sim.track import declare_track_params, generate_cones


def yaw_from_quaternion(q) -> float:
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))


class FakePerception(Node):
    def __init__(self):
        super().__init__('fake_perception')
        self.cones = generate_cones(declare_track_params(self))

        self.range = self.declare_parameter('range', 50.0).value
        self.half_fov = math.radians(self.declare_parameter('fov_deg', 120.0).value) / 2.0
        self.noise_std = self.declare_parameter('noise_std', 0.0).value
        self.miss_probability = self.declare_parameter('miss_probability', 0.0).value
        self.map_frame = self.declare_parameter('map_frame', 'map').value
        self.base_frame = self.declare_parameter('base_frame', 'base_link').value
        rate = self.declare_parameter('rate', 10.0).value
        self.rng = random.Random(self.declare_parameter('seed', 0).value)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pub = self.create_publisher(ConeArray, '/perception/cones', 10)
        self.timer = self.create_timer(1.0 / rate, self.on_timer)

    def on_timer(self):
        try:
            tf = self.tf_buffer.lookup_transform(self.map_frame, self.base_frame, Time())
        except TransformException as e:
            self.get_logger().warn(f'No vehicle pose yet: {e}', throttle_duration_sec=2.0)
            return

        px = tf.transform.translation.x
        py = tf.transform.translation.y
        yaw = yaw_from_quaternion(tf.transform.rotation)
        c, s = math.cos(yaw), math.sin(yaw)

        detections = []
        for cone in self.cones:
            dx, dy = cone.x - px, cone.y - py
            lx = c * dx + s * dy
            ly = -s * dx + c * dy
            dist = math.hypot(lx, ly)
            if dist > self.range or abs(math.atan2(ly, lx)) > self.half_fov:
                continue
            if self.rng.random() < self.miss_probability:
                continue
            if self.noise_std > 0.0:
                lx += self.rng.gauss(0.0, self.noise_std)
                ly += self.rng.gauss(0.0, self.noise_std)
            detections.append((dist, lx, ly, cone.color))
        detections.sort(key=lambda d: d[0])

        msg = ConeArray()
        msg.header.stamp = tf.header.stamp
        msg.header.frame_id = self.base_frame
        for _, lx, ly, color in detections:
            cone = Cone()
            cone.position.x = lx
            cone.position.y = ly
            cone.color = color
            msg.cones.append(cone)
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = FakePerception()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
