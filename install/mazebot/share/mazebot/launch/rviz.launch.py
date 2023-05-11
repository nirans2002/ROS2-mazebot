import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='mazebot',
            executable='talker',
            name='Publisher',
            output='screen'
        ),   Node(
            package='mazebot',
            executable='listener',
            name='Listener',
            output='screen'
        ),
    ])