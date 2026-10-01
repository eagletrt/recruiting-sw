"""Internal launch for developing the sim. Not part of the candidate deliverable."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('eagle_sim')
    params = os.path.join(share, 'config', 'track.yaml')
    rviz_cfg = os.path.join(share, 'rviz', 'base.rviz')

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        Node(package='eagle_sim', executable='track_publisher', parameters=[params]),
        Node(package='eagle_sim', executable='fake_perception', parameters=[params]),
        Node(package='eagle_sim', executable='vehicle_sim', parameters=[params]),
        Node(package='eagle_sim', executable='lateral_controller', parameters=[params]),
        Node(package='eagle_sim', executable='can_gateway', parameters=[params]),
        Node(package='rviz2', executable='rviz2', arguments=['-d', rviz_cfg],
             condition=IfCondition(LaunchConfiguration('rviz'))),
    ])
