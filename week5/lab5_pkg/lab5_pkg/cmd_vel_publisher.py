import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 2.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.moving_forward = True

    def timer_callback(self):
        msg = Twist()
        if self.moving_forward:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.get_logger().info('Publishing forward velocity: "%s"' % msg.linear.x)
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Publishing zero velocity: "%s"' % msg.linear.x)
        
        self.publisher_.publish(msg)
        self.moving_forward = not self.moving_forward

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_publisher = CmdVelPublisher()
    rclpy.spin(cmd_vel_publisher)
    cmd_vel_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
