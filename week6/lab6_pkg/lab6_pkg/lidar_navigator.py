import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

class LidarNavigator(Node):
    def __init__(self):
        super().__init__('lidar_navigator')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Define thresholds
        self.front_threshold = 0.5  # meters
        self.side_threshold = 0.3   # meters

    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        
        # -----------------------------
        # TODO 1: Clean data (remove inf/nan)
        # -----------------------------
        ranges = np.nan_to_num(ranges, nan=10.0, posinf=10.0, neginf=10.0)
        
        # -----------------------------
        # TODO 2: Define regions
        # -----------------------------
        # Front region is usually the first 15 and last 15 degrees
        front = np.concatenate((ranges[:15], ranges[345:]))
        # Left region is around 90 degrees
        left = ranges[60:120]
        # Right region is around 270 degrees
        right = ranges[240:300]
        
        # Compute minimum distance
        front_dist = np.min(front)
        left_dist = np.min(left)
        right_dist = np.min(right)
        
        # Debug printing
        self.get_logger().info(f"Front: {front_dist:.2f}, Left: {left_dist:.2f}, Right: {right_dist:.2f}")

        twist = Twist()
        
        # -----------------------------
        # TODO 3: Obstacle logic
        # -----------------------------
        if front_dist < self.front_threshold:
            # obstacle in front
            twist.linear.x = 0.0
            
            # -------------------------
            # TODO 4: Turn direction
            # -------------------------
            if left_dist > right_dist:
                twist.angular.z = 0.5   # left clearer
            else:
                twist.angular.z = -0.5  # right clearer
        else:
            # -------------------------
            # TODO 5: Forward motion
            # -------------------------
            twist.linear.x = 0.2
            
            # Simple wall following logic
            if left_dist < self.side_threshold:
                twist.angular.z = -0.2  # too close to left wall, turn right slightly
            elif right_dist < self.side_threshold:
                twist.angular.z = 0.2   # too close to right wall, turn left slightly
            else:
                twist.angular.z = 0.0

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = LidarNavigator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
