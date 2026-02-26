Q1:

Node: A node is an executable in ROS 2 that performs computation, such as publishing or subscribing to data.

Topic: A topic is a named channel over which nodes exchange messages in ROS 2.

Package: A package is a collection of ROS 2 files, including nodes, configuration, and dependencies, organized for a specific functionality.

Workspace: A workspace is a directory where multiple ROS 2 packages are developed, built, and managed together.

Q2:

Sourcing a workspace sets up the environment variables so ROS 2 can find your packages and executables; without sourcing, ROS 2 commands may fail because it won’t recognize your workspace or nodes.

Q3:

colcon build compiles all packages in the workspace, resolving dependencies, and generates build/, install/, and log/ directories for compiled code, installed files, and build logs, respectively.

Q4:

It defines the command-line executable that runs a specific Python node when invoked, allowing you to launch a node with a simple command.

Q5:

+------------+         Topic: /chatter         +------------+
| Publisher  | ------------------------------> | Subscriber |
+------------+                                 +------------+

The publisher sends messages on the topic /chatter.
The subscriber receives messages from the same topic.
