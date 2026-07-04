"""
Launch file for Four-Bar Linkage Mechanism Visualization
=========================================================
This launch file starts:
1. robot_state_publisher - Publishes the URDF robot model to /robot_description
2. joint_state_publisher - Custom node that publishes oscillatory joint states
3. rviz2 - 3D visualization tool

Usage:
  ros2 launch four_bar_linkage display.launch.py
"""

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get package share directory
    pkg_share = get_package_share_directory('four_bar_linkage')

    # URDF file path
    urdf_file = os.path.join(pkg_share, 'urdf', 'four_bar_linkage.urdf')

    # RViz config file path
    rviz_config_file = os.path.join(pkg_share, 'config', 'rviz_config.rviz')

    # Read URDF content
    with open(urdf_file, 'r') as f:
        robot_description_content = f.read()

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': False
        }]
    )

    # Custom Joint State Publisher Node (oscillatory motion)
    joint_state_publisher_node = Node(
        package='four_bar_linkage',
        executable='joint_state_publisher',
        name='four_bar_joint_state_publisher',
        output='screen'
    )

    # RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])
