import rclpy
from rclpy.node import Node
import os

def main():
    rclpy.init()
    node = Node('simple_node')

    # Declare parameter
    node.declare_parameter('student_name', '')

    name = node.get_parameter('student_name').get_parameter_value().string_value

    if name:
        node.get_logger().info(f'Student Name: {name}')
    else:
        node.get_logger().info('student_name not set')

    rclpy.shutdown()

if __name__ == '__main__':
    main()
