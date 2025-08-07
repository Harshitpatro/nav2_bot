#!/usr/bin/env python3

from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declare use_sim_time argument
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([
            FindPackageShare("testbed_description"),
            "urdf",
            "testbed.xacro",
            ]),
    ])

    robot_description = {"robot_description": robot_description_content}
    return LaunchDescription([
        declare_use_sim_time_cmd,
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}]
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                robot_description, 
                {
                    'use_sim_time': use_sim_time,
                    'publish_frequency': 50.0,  # Increase publish frequency
                    'ignore_timestamp': False   # Ensure proper timestamp handling
                }
            ]),
    ])