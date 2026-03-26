import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class GoalTurtle(Node):
    def __init__(self):
        super().__init__('goal_turtle')
        self.pose = Pose()
        self.goal_reached = False
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.create_timer(0.1, self.go_to_goal)
        self.get_logger().info('Going to goal (8.0, 8.0)!')

    def pose_callback(self, msg):
        self.pose = msg

    def go_to_goal(self):
        if self.goal_reached:
            return
        msg = Twist()
        target_x = 8.0
        target_y = 8.0
        dx = target_x - self.pose.x
        dy = target_y - self.pose.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0.1:
            angle = math.atan2(dy, dx)
            error = math.atan2(
                math.sin(angle - self.pose.theta),
                math.cos(angle - self.pose.theta))
            msg.linear.x = min(1.5, distance)
            msg.angular.z = 2.0 * error
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.goal_reached = True
            self.get_logger().info('Goal Reached!')
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GoalTurtle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()