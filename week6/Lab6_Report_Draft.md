# Lab Manual 6 Report: Reactive Navigation Using TurtleBot3 LiDAR

## 1. Steps Followed to Complete Tasks
1. Set up the environment by setting `TURTLEBOT3_MODEL=burger` and sourcing the workspace.
2. Launched TurtleBot3 in Gazebo.
3. Created a ROS 2 Python package `lab6_pkg` containing the `lidar_navigator` node.
4. Filled in the boilerplate code for `lidar_navigator.py`:
   - Cleaned `/scan` data using `numpy.nan_to_num`.
   - Extracted front, left, and right regions using array slicing.
   - Wrote conditional logic to stop when `front_distance < 0.5` and turn towards the clearest path.
5. Built the package and ran the node.
6. Visualized the robot's reactions to obstacles in Gazebo.
7. Visualized the `/scan` and robot models in RViz.
8. Used `rqt_graph` to verify topics and nodes.

## 2. RViz Visualization
shared in screenshots

## 3. rqt_graph
shared in screenshots

## 4. Robot Behaviors (Screenshots/Videos)

- Robot stopping at an obstacle
- Robot avoiding an obstacle
- Robot navigating without collision

## 5. Observations
## Robot Behavior Near Obstacles
- When the robot approached an obstacle head-on, it successfully stopped at approximately 0.5 meters (the configured `front_threshold`) and initiated a turn toward the side with greater clearance.
- The robot was able to detect walls and cylindrical obstacles in the TurtleBot3 world using the 360-degree LiDAR scan data published on the `/scan` topic.
- The wall-following logic (using `side_threshold = 0.3m`) helped the robot make minor corrections when drifting too close to a wall during forward motion.

### Oscillations and Instability
- A significant observation was that the robot experienced **oscillation** when trapped in tight corners or between closely spaced obstacles. This occurred because the decision logic re-evaluated the turn direction on every scan callback cycle (~10 Hz). In a corner, the left and right distances kept alternating as the "better" option, causing the robot to jitter back and forth without escaping.
- This highlights the importance of **state-based control** — committing to a turn direction until the front is clear, rather than re-deciding every cycle.

### Effect of Changing Threshold Values
- **Increasing `front_threshold` to 0.8m:** The robot began turning much earlier, making it safer but overly cautious. It struggled to pass through narrow corridors where the gap was less than 0.8m wide.
- **Decreasing `front_threshold` to 0.3m:** The robot drove closer to obstacles before reacting, which increased the risk of collision, especially at higher speeds due to the reaction delay.
- **Increasing angular speed from 0.5 to 0.8 rad/s:** The robot escaped corners faster but its motion appeared jerky and less smooth.
- The optimal balance for the TurtleBot3 world was found to be a front threshold of **0.5m** with a turning speed of **0.5 rad/s**.

## 6. Code: lidar_navigator.py
```python
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
        
        # Clean data (remove inf/nan)
        ranges = np.nan_to_num(ranges, nan=10.0, posinf=10.0, neginf=10.0)
        
        # Define regions
        front = np.concatenate((ranges[:15], ranges[345:]))
        left = ranges[60:120]
        right = ranges[240:300]
        
        # Compute minimum distance
        front_dist = np.min(front)
        left_dist = np.min(left)
        right_dist = np.min(right)

        twist = Twist()
        
        # Obstacle logic
        if front_dist < self.front_threshold:
            # obstacle in front
            twist.linear.x = 0.0
            
            # Turn direction
            if left_dist > right_dist:
                twist.angular.z = 0.5   # left clearer
            else:
                twist.angular.z = -0.5  # right clearer
        else:
            # Forward motion
            twist.linear.x = 0.2
            
            # Simple wall following logic
            if left_dist < self.side_threshold:
                twist.angular.z = -0.2  # too close to left wall, turn right
            elif right_dist < self.side_threshold:
                twist.angular.z = 0.2   # too close to right wall, turn left
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
```

## 7. Conclusion

This lab provided hands-on experience in implementing reactive navigation using LiDAR sensor data from the `/scan` topic. The key learning outcomes were:

1. **LiDAR Data Interpretation:** We learned that the `/scan` topic publishes a `LaserScan` message containing an array of 360 distance values (one per degree), which must be cleaned of `inf` and `NaN` values before processing.
2. **Region Extraction:** By slicing the ranges array into front (0°±15°), left (60°–120°), and right (240°–300°) regions, we were able to extract directional distance information and compute the minimum distance in each region for decision-making.
3. **Reactive Control:** A simple `if/else` structure was sufficient to implement obstacle avoidance — stopping when the front distance fell below a threshold and turning toward the clearer side.
4. **Wall Following:** Proportional corrections based on side distances allowed the robot to maintain a safe distance from walls during forward motion.

The main challenge faced was **oscillation in tight spaces**, where the robot would rapidly alternate between turning left and right without making progress. This demonstrated that purely reactive navigation, while effective in open environments, has limitations in confined spaces and would benefit from state-based decision-making or more advanced path-planning algorithms. Overall, this lab built a strong foundation for understanding how raw sensor data can be converted into real-time control decisions for autonomous mobile robots.

