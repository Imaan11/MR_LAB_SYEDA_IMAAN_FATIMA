import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class TurtleTask1(Node):

    def __init__(self):
        super().__init__('turtle_task1')

        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        self.dt = 0.1
        self.timer = self.create_timer(self.dt, self.update)

        self.time = 0.0

        # State control
        self.mode = "circle"   # switch later

        # Triangle control
        self.tri_state = "move"
        self.tri_time = 0.0

        # Parameters
        self.linear_speed = 1.0
        self.angular_speed = 1.0

        self.turn_time = (2 * math.pi / 3) / self.angular_speed  # 120 deg
        self.edge_time = 2.0

    def update(self):

        msg = Twist()
        self.time += self.dt

        # -------- Mode Switching --------
        if self.time > 10.0:   # after 10 sec switch to triangle
            self.mode = "triangle"

        # -------- Circle --------
        if self.mode == "circle":
            msg.linear.x = 1.5
            msg.angular.z = 1.0

        # -------- Triangle --------
        elif self.mode == "triangle":

            self.tri_time += self.dt

            if self.tri_state == "move":
                msg.linear.x = self.linear_speed

                if self.tri_time >= self.edge_time:
                    self.tri_state = "turn"
                    self.tri_time = 0.0

            elif self.tri_state == "turn":
                msg.angular.z = self.angular_speed

                if self.tri_time >= self.turn_time:
                    self.tri_state = "move"
                    self.tri_time = 0.0

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleTask1()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()