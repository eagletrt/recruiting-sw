"""Acceleration track layout shared by all sim nodes.

The vehicle starts at the map origin facing +x. Blue cones are on the left (+y),
yellow on the right (-y). The stop zone is the box between the four big orange
cones placed at x = straight_length and x = straight_length + stop_zone_length.
"""
from dataclasses import dataclass

from eagle_msgs.msg import Cone


@dataclass(frozen=True)
class TrackConfig:
    straight_length: float = 75.0
    track_width: float = 4.0
    cone_spacing: float = 5.0
    stop_zone_length: float = 10.0


@dataclass(frozen=True)
class TrackCone:
    x: float
    y: float
    color: int


@dataclass(frozen=True)
class StopZone:
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def contains(self, x: float, y: float) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max


def declare_track_params(node) -> TrackConfig:
    defaults = TrackConfig()
    return TrackConfig(
        straight_length=node.declare_parameter('track.straight_length', defaults.straight_length).value,
        track_width=node.declare_parameter('track.track_width', defaults.track_width).value,
        cone_spacing=node.declare_parameter('track.cone_spacing', defaults.cone_spacing).value,
        stop_zone_length=node.declare_parameter('track.stop_zone_length', defaults.stop_zone_length).value,
    )


def generate_cones(cfg: TrackConfig) -> list[TrackCone]:
    half = cfg.track_width / 2.0
    cones = []
    x = 0.0
    while x < cfg.straight_length - 1e-6:
        cones.append(TrackCone(x, half, Cone.BLUE))
        cones.append(TrackCone(x, -half, Cone.YELLOW))
        x += cfg.cone_spacing
    for x in (cfg.straight_length, cfg.straight_length + cfg.stop_zone_length):
        cones.append(TrackCone(x, half, Cone.ORANGE_BIG))
        cones.append(TrackCone(x, -half, Cone.ORANGE_BIG))
    return cones


def stop_zone(cfg: TrackConfig) -> StopZone:
    half = cfg.track_width / 2.0
    return StopZone(cfg.straight_length, cfg.straight_length + cfg.stop_zone_length, -half, half)
