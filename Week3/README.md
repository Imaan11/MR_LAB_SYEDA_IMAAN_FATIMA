# Week 3 – Mobile Robotics Lab (ROS 2 & Turtlesim)

## Overview
This week's lab focused on understanding and implementing the **publisher-subscriber model in ROS 2** using the turtlesim simulator. The objective was to move from basic terminal-based control to developing **custom ROS 2 nodes** for controlling turtle motion programmatically.


## Tasks Performed

### 1. Motion Control using Publisher
- Implemented a ROS 2 node to publish velocity commands (`geometry_msgs/Twist`) 
- Controlled turtle movement through:
  - Linear velocity (`linear.x`)
  - Angular velocity (`angular.z`)
- Achieved:
  - Circular motion 
  - Triangular trajectory using state-based logic 

---

### 2. Multi-Turtle Coordination
- Spawned multiple turtles using the `/spawn` service 
- Created separate publishers for:
  - `turtle1`
  - `turtle2`
  - `turtle3`
- Implemented simultaneous motion patterns:
  - Circle 
  - Square 
  - Triangle 

---

### 3. Position Control
- Moved turtle to a specific location using velocity commands 
- Gained understanding of:
  - How motion relates to position over time 
  - Limitations of open-loop (time-based) control 

---

## Key ROS 2 Concepts Learned

- Publisher-Subscriber architecture 
- Creating custom ROS 2 nodes in Python (`rclpy`) 
- Using topics:
  - `/turtle1/cmd_vel` 
- Using services:
  - `/spawn` 
- Understanding motion control using velocity commands 




