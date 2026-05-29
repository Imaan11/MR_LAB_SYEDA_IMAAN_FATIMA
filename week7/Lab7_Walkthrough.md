# Lab 7 Walkthrough – Autonomous Navigation with Nav2 & Multi-Waypoint Mission Planning

## 📖 Lab Manual Explained

### What This Lab Is About
Lab 7 is the **continuation of Lab 5**. In Lab 5 you built a map with SLAM/Cartographer.
In Lab 7 you **use that map** to make the robot navigate autonomously — no joystick needed.

The big picture pipeline:

```
Saved Map (pgm+yaml)
        │
        ▼
  Map Server  ←── loaded into Nav2
        │
        ▼
  AMCL          ←── figures out WHERE the robot is on the map
        │
        ▼
  Planner Server  ←── draws a global path to the goal
        │
        ▼
  Controller Server ←── follows that path in real time
        │
        ▼
  Robot moves!
```

### Key Nav2 Components (simplified)

| Component | Role |
|---|---|
| **Map Server** | Loads `my_map.pgm` + `my_map.yaml` and publishes the occupancy grid |
| **AMCL** | Uses LiDAR + particle filter to estimate robot pose on the map |
| **Planner Server** | Computes global path (A* / NavFn) from current pose to goal |
| **Controller Server** | Follows the path locally in real time (DWB controller) |
| **BT Navigator** | Orchestrates all servers using a Behaviour Tree |
| **Waypoint Follower** | Takes a list of goals and executes them in sequence |
| **Recovery / Behavior Server** | When stuck: spin, back up, or wait |

---

## 🏗️ Package Structure Built

```
ros2_ws_imaan/src/lab7_pkg/
├── lab7_pkg/
│   ├── __init__.py
│   ├── waypoint_navigator.py          ← Task 2 (hardcoded 5 waypoints)
│   └── waypoint_navigator_dynamic.py  ← Task 3 (CLI argument waypoints)
├── resource/
│   └── lab7_pkg
├── package.xml
├── setup.cfg
└── setup.py
```

---

## 🚀 Step-by-Step Walkthrough

> **Open a fresh terminal for EACH step below** (T1, T2, T3 …).
> Always source ROS and export the robot model first.

### Every Terminal – Run These First
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws_imaan/install/setup.bash
export TURTLEBOT3_MODEL=burger
```
> **Tip:** Add those 3 lines to `~/.bashrc` so you never need to repeat them:
> ```bash
> echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
> echo "source ~/ros2_ws_imaan/install/setup.bash" >> ~/.bashrc
> echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
> ```

---

### Step 1 – Check Your Map Exists (Lab 5 output)
```bash
ls ~/maps/
# Expected: my_map.pgm   my_map.yaml
```
If the folder is missing, you need to re-run Lab 5 SLAM and save the map first.

---

### Step 2 (T1) – Launch Gazebo with TurtleBot3 World
```bash
# Terminal 1
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```
Wait until Gazebo fully loads and the burger robot appears in the world.

> **Important:** The robot must spawn at **(0, 0, 0)** — the same origin used during Lab 5 SLAM.

---

### Step 3 (T2) – Launch Nav2 with Your Saved Map
```bash
# Terminal 2
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  use_sim_time:=True \
  map:=$HOME/maps/my_map.yaml
```
This starts:
- Map Server → loads `my_map.yaml`
- AMCL → initializes particle cloud
- Planner + Controller → ready for goals
- RViz → opens with Nav2 panels

---

### Step 4 – Set Initial Pose in RViz
1. In RViz, click **"2D Pose Estimate"** in the toolbar
2. Click on the map at the robot's actual position (usually near the origin)
3. **Drag the arrow** in the direction the robot faces (usually +X axis)
4. You should see a cluster of **red arrows** (particle cloud) appear around that spot

**Verify localization (T3):**
```bash
# Terminal 3
ros2 topic echo /amcl_pose
```
The pose should read approximately `x: 0.0, y: 0.0`.

**Optional – drive to help AMCL converge (T4):**
```bash
# Terminal 4
ros2 run turtlebot3_teleop teleop_keyboard
```
Drive a short distance forward/backward — the particle cloud will tighten up.

> ✅ **Good localization check:** The yellow/green laser scan lines in RViz should align
> perfectly with the black walls on the map. If they don't, re-set the pose estimate.

---

### Step 5 (T5) – Inspect Running Nodes
```bash
# Terminal 5
rqt_graph
```
You should see nodes: `nav2_container`, `amcl`, `map_server`, `bt_navigator`,
`planner_server`, `controller_server`, `waypoint_follower` all connected via topics.

---

## ✅ Task Walkthroughs

---

### Task 1 – Single Goal Navigation

**Via RViz (easiest):**
1. Click **"Nav2 Goal"** button in the toolbar
2. Click a free (white) space on the map and drag to set orientation
3. Watch the global path (green line) appear and the robot move

**Via Command Line:**
```bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.0, y: 0.5, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}"
```

**Record pose before/after (for your report):**
```bash
ros2 topic echo /amcl_pose --once
```

---

### Task 2 – Multi-Waypoint Mission (5 Hardcoded Waypoints)

**Your waypoint table to fill in:**

| WP# | X (m) | Y (m) | Z (m) | orientation_w | Description |
|-----|--------|--------|--------|---------------|-------------|
| 1 | 0.5 | 0.0 | 0.0 | 1.0 | Slightly forward |
| 2 | 1.0 | 0.5 | 0.0 | 1.0 | Move right |
| 3 | 1.5 | 0.0 | 0.0 | 1.0 | Further forward |
| 4 | 1.0 | -0.5 | 0.0 | 1.0 | Swing left |
| 5 | 0.0 | 0.0 | 0.0 | 1.0 | Return to origin |

> **Tip:** Use `ros2 topic echo /amcl_pose` to confirm the robot's current coordinates
> and pick waypoints in free space that you can verify in RViz.

**Run the node:**
```bash
# Terminal (with Gazebo + Nav2 already running)
ros2 run lab7_pkg waypoint_navigator
```

Expected output:
```
[INFO] [waypoint_navigator]: === Lab 7 Waypoint Mission Starting ===
[INFO] [waypoint_navigator]: Waiting for FollowWaypoints action server...
[INFO] [waypoint_navigator]: Sending 5 waypoints to Nav2...
[INFO] [waypoint_navigator]: Goal ACCEPTED. Robot is navigating...
[INFO] [waypoint_navigator]:   → Navigating to waypoint #0
[INFO] [waypoint_navigator]:   → Navigating to waypoint #1
...
[INFO] [waypoint_navigator]: SUCCESS – All waypoints reached! Mission complete.
```

---

### Task 3 – Dynamic Waypoint Injection via CLI

Each group of 3 values = one waypoint: `x  y  orientation_w`

**Example (3 waypoints):**
```bash
ros2 run lab7_pkg waypoint_navigator_dynamic -- \
  0.5 0.0 1.0 \
  1.0 0.5 1.0 \
  0.0 0.0 1.0
```

**Example (5 waypoints – same as Task 2):**
```bash
ros2 run lab7_pkg waypoint_navigator_dynamic -- \
  0.5 0.0 1.0 \
  1.0 0.5 1.0 \
  1.5 0.0 1.0 \
  1.0 -0.5 1.0 \
  0.0 0.0 1.0
```

> **Note the `--`** between `ros2 run lab7_pkg waypoint_navigator_dynamic` and the
> numbers. This tells ROS 2 to stop parsing its own flags and pass the rest to Python.

---

### Task 4 – Costmap Observation

**List all costmap topics:**
```bash
ros2 topic list | grep costmap
```

| Topic | Description |
|---|---|
| `/global_costmap/costmap` | Full map + inflation used by global planner |
| `/global_costmap/costmap_updates` | Incremental updates to global costmap |
| `/local_costmap/costmap` | Rolling window around robot used by DWB controller |
| `/local_costmap/costmap_updates` | Incremental updates to local costmap |

**In RViz** → Add the `Map` display and point it at `/local_costmap/costmap`.
Drive the robot close to a wall and watch the orange/red inflation zone expand.

---

### Task 5 – Recovery Behaviors

1. In Gazebo, go to **Insert** panel → drag a **Box** model in front of the robot's planned path
2. Watch RViz — Nav2 will first attempt to replan around it
3. If replanning fails, it triggers recovery: **spin → back up → wait → replan**
4. Open `rqt_graph` and look for the **`behavior_server`** node — this is the recovery handler

**Identify recovery topic:**
```bash
ros2 topic list | grep recovery
ros2 node list | grep behavior
```

---

## 📸 RViz Panels to Enable (for Screenshots / Deliverables)

Go to **Add** in the Displays panel and enable:

| Display | Topic |
|---|---|
| Map | `/map` |
| Global Costmap | `/global_costmap/costmap` |
| Local Costmap | `/local_costmap/costmap` |
| Path (Global) | `/plan` |
| Path (Local) | `/local_plan` |
| PoseArray (AMCL particles) | `/particle_cloud` |
| LaserScan | `/scan` |
| TF | (auto) |
| Odometry | `/odom` |

Set **Fixed Frame → `map`** in Global Options.

---

## 📦 Deliverables Checklist

| # | Deliverable | How |
|---|---|---|
| 1 | Short report with observations | Write after completing each step |
| 2 | Completed waypoint table (5 WPs) | Fill in the Task 2 table above |
| 3 | `waypoint_navigator.py` source | ✅ Already in `lab7_pkg` |
| 4 | `waypoint_navigator_dynamic.py` source | ✅ Already in `lab7_pkg` |
| 5 | RViz screenshots: map + AMCL particles, global/local paths, robot at each WP, costmaps | Screenshot during Task 2 run |
| 6 | `rqt_graph` screenshot showing Nav2 nodes | Run `rqt_graph` in Step 5 |
| 7 | Recovery behavior observations | Document Task 5 |
| 8 | Conclusion comparing SLAM (Lab 5) vs Navigation (Lab 7) | Final written section |

---

## 🔧 Quick Troubleshooting

| Problem | Fix |
|---|---|
| `FollowWaypoints` server not found | Make sure Nav2 is running (Step 3) |
| Laser scan doesn't align with map | Re-do **2D Pose Estimate** in RViz |
| Robot won't move / path fails | Check `TURTLEBOT3_MODEL=burger` is exported |
| `nav2_msgs` not found | `sudo apt install ros-humble-navigation2` |
| Robot collides immediately | AMCL pose was not set — set it first |
| Waypoint rejected | Waypoint may be inside an obstacle; pick a white space in RViz |
