import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('Odometry Subscriber started. Listening on /odom ...')

    def listener_callback(self, msg):
        # --- Position ---
        pos_x = msg.pose.pose.position.x
        pos_y = msg.pose.pose.position.y
        pos_z = msg.pose.pose.position.z

        # --- Orientation: quaternion -> yaw (rotation about Z) ---
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        # --- Twist (velocities) ---
        lin_x = msg.twist.twist.linear.x
        lin_y = msg.twist.twist.linear.y
        ang_z = msg.twist.twist.angular.z

        self.get_logger().info(
            f'\n--- Odometry Message ---\n'
            f'  Position  : x={pos_x:.4f}  y={pos_y:.4f}  z={pos_z:.4f}\n'
            f'  Yaw (rad) : {yaw:.4f}  ({math.degrees(yaw):.2f} deg)\n'
            f'  Lin. Vel  : x={lin_x:.4f}  y={lin_y:.4f}\n'
            f'  Ang. Vel  : z={ang_z:.4f}\n'
            f'  Frame     : {msg.header.frame_id}'
        )

def main(args=None):
    rclpy.init(args=args)
    odom_subscriber = OdomSubscriber()
    rclpy.spin(odom_subscriber)
    odom_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

