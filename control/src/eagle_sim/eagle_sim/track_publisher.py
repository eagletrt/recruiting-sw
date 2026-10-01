"""Publishes the ground-truth track (cones, asphalt, stop zone) for RViz."""
import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from visualization_msgs.msg import Marker, MarkerArray

from eagle_msgs.msg import Cone
from eagle_sim.track import declare_track_params, generate_cones, stop_zone

# (diameter, height) in metres, FS rules cone sizes
CONE_SIZE = {
    Cone.BLUE: (0.228, 0.325),
    Cone.YELLOW: (0.228, 0.325),
    Cone.ORANGE_SMALL: (0.228, 0.325),
    Cone.ORANGE_BIG: (0.285, 0.505),
}
CONE_RGB = {
    Cone.BLUE: (0.05, 0.25, 0.9),
    Cone.YELLOW: (1.0, 0.85, 0.0),
    Cone.ORANGE_SMALL: (1.0, 0.45, 0.0),
    Cone.ORANGE_BIG: (1.0, 0.45, 0.0),
}


def make_marker(frame, ns, marker_id, marker_type, pos, scale, rgba):
    m = Marker()
    m.header.frame_id = frame
    m.ns = ns
    m.id = marker_id
    m.type = marker_type
    m.action = Marker.ADD
    m.pose.position.x, m.pose.position.y, m.pose.position.z = pos
    m.pose.orientation.w = 1.0
    m.scale.x, m.scale.y, m.scale.z = scale
    m.color.r, m.color.g, m.color.b, m.color.a = rgba
    return m


class TrackPublisher(Node):
    def __init__(self):
        super().__init__('track_publisher')
        cfg = declare_track_params(self)
        frame = self.declare_parameter('map_frame', 'map').value

        markers = MarkerArray()
        for i, cone in enumerate(generate_cones(cfg)):
            d, h = CONE_SIZE[cone.color]
            markers.markers.append(make_marker(
                frame, 'cones', i, Marker.CYLINDER,
                (cone.x, cone.y, h / 2.0), (d, d, h), (*CONE_RGB[cone.color], 1.0)))

        margin = 10.0
        length = cfg.straight_length + cfg.stop_zone_length + 2.0 * margin
        markers.markers.append(make_marker(
            frame, 'asphalt', 0, Marker.CUBE,
            (length / 2.0 - margin, 0.0, -0.01), (length, cfg.track_width + 6.0, 0.01),
            (0.25, 0.25, 0.27, 1.0)))

        zone = stop_zone(cfg)
        markers.markers.append(make_marker(
            frame, 'stop_zone', 0, Marker.CUBE,
            ((zone.x_min + zone.x_max) / 2.0, 0.0, 0.0),
            (zone.x_max - zone.x_min, zone.y_max - zone.y_min, 0.01),
            (0.1, 0.8, 0.2, 0.35)))

        qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.pub = self.create_publisher(MarkerArray, '/sim/track', qos)
        self.pub.publish(markers)


def main():
    rclpy.init()
    node = TrackPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
