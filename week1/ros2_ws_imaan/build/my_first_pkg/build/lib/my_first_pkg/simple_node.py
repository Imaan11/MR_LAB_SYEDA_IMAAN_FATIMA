import rclpy
from rclpy.node import Node
import os

def main():
    rclpy.init()
    node = Node('simple_node')

    # ---------- Task 1: Custom message ----------
    node.get_logger().info('Welcome to Mobile Robotics Lab')

    # ---------- Task 2: Persistent counter ----------
    counter_file = os.path.join(os.path.dirname(__file__), 'counter.txt')

    if os.path.exists(counter_file):
        with open(counter_file, 'r') as f:
            count = int(f.read())
    else:
        count = 0

    count += 1

    with open(counter_file, 'w') as f:
        f.write(str(count))

    node.get_logger().info(f'Run count: {count}')

    # ---------- Task 3: ROS parameter ----------
    node.declare_parameter('student_name', '')
    name = node.get_parameter('student_name').get_parameter_value().string_value

    if name:
        node.get_logger().info(f'Student Name: {name}')
    else:
        node.get_logger().info('student_name not set')

    rclpy.shutdown()

if __name__ == '__main__':
    main()
