import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """
    Launch file for Lab 8: URDF Visualization in RViz.
    Starts:
      - robot_state_publisher  (reads URDF, publishes /tf)
      - joint_state_publisher_gui  (provides joint state sliders)
      - rviz2  (with pre-configured display config)
    """

    pkg_share = get_package_share_directory('my_robot_description')
    urdf_file = os.path.join(pkg_share, 'urdf', 'my_robot.urdf')
    rviz_config = os.path.join(pkg_share, 'rviz', 'my_robot.rviz')

    # Read URDF content into a string for robot_state_publisher
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # ── Nodes ────────────────────────────────────────────────────────────────

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': False,
        }]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz2_node,
    ])
