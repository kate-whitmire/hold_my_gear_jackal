# Overview

This repository contains the software to run a person-following demo on a Clearpath Robotics Jackal UGV (J100) using a RealSense D435 depth camera and YOLO object detection. The demo is operated entirely from a laptop via a PyQt5 GUI — no terminal knowledge required for the end user once setup is completed.This repository was forked from a previous project that was focused on people-following with the use of Nav2 for path planning and object avoidance. The files relevant to that project are included below but are not related to the demo.

## Repo Layout

```
hold_my_gear_jackal/
├── src/
│   └── jackal_yolo_follow/
│       ├── jackal_yolo_follow/
│       │   ├── __init__.py
│       │   ├── circle_drive.py          # Spin-in-place node
│       │   ├── follow_mode_gui.py       # Main demo GUI (most relevant to demo)
│       │   ├── gui_styles.py            # GUI styling, password dialog, widget layout
│       │   ├── nav_to_pose_test.py      # Nav2 person-following node (navigation, pt. 1)
│       │   ├── yolo_follower.py         # YOLO person-following node
│       │   └── yolo_nav2_follower.py    # Nav2 person-following node (vision, pt. 2)
│       ├── launch/
│       │   ├── regular_follow_mode_launch.py   # Following demo launch file
│       │   ├── nav2_follow_mode_launch.py
│       │   └── rviz_launch.py
│       ├── resource/
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── .gitignore
├── Jackal Image.png                     # Desktop icon image
├── JackalDemo.desktop                   # Desktop launcher file
├── dependencies.repos
├── robot.yaml                           # Clearpath robot configuration
├── run_demo.sh                          # Shell script launched by desktop icon
└── setup.bash                           # Laptop workspace setup script
```

## System Overview

### Hardware
- **Robot:** Clearpath Robotics Jackal UGV (J100)
- **Sensor:** Intel RealSense D435 depth camera
- **Operator computer:** Personal laptop running Ubuntu, connected to the same network as the robot

### Software
- **ROS 2 Jazzy** on both the robot and laptop
- **YOLO (Ultralytics yolo11n)** for person detection, running inside a Python virtual environment (`~/vision_venv`) on the robot
- **SLAM Toolbox** for mapping (optional, used with RViz)
- **depthimage_to_laserscan** for converting depth images to laser scans for SLAM
- **PyQt5** for the operator GUI on the laptop


## Navigation

### Velocity Follower (`yolo_follower.py`)
The primary demo mode. Uses the RealSense D435 to detect people with YOLO and follows the closest detected person by publishing `TwistStamped` velocity commands to `/j100_0000/cmd_vel`. Key behaviors:

- Follows at a configurable target distance (default 1.5m)
- Backs up if the person gets too close
- Emergency forward stop if anything enters the minimum distance threshold in front of the camera
- Smoothed velocity transitions to avoid jerky motion
- Depth averaging over a patch to reduce noisy sensor readings

### Circle Drive (`circle_drive.py`)
Spins the robot in place by publishing a constant angular velocity to `/j100_0000/cmd_vel`. Useful for demos when you want the robot visually active without following anyone.

## Follower Demo

The demo is operated from the laptop via a PyQt5 GUI. The operator:
1. Double-clicks the **Jackal Demo** desktop icon
2. Enters the robot SSH password
3. Clicks **Start: Follow Mode** or **Start: Drive in Circle**
4. Optionally clicks **Open RViz** for a live map view
5. Clicks **Close All Nodes** to shut everything down cleanly


### How It Works
The laptop runs the GUI locally. When the operator clicks the desktop icon called 'Jackal Demo' or runs the GUI file, the GUI prompts the user to SSH into the robot and has four buttons to choose from. The first button starts follow mode, which launches 'regular_follow_mode.py'. This spins up the depth camera on the robot and allows the robot to start identifying and tracking people. Once it finds a person in frame, it will drive towards them and stop about a foot away. The robot should back up when you approach it and stop driving if it detects you are too close, but as with any autonomous system take care to be aware of the robot as it moves around you. 

The next button runs 'circle_drive.py', which has the robot spin in place indefinitely. The third button is Open Rviz, which launches slam on the robot and opens Rviz on the user's computer. It's important to note that Follow Mode should be run beforehand because it turns on the depth camera, which slam needs to create a map. This is intended as a fun visual feature to see how the robot views its surroundings as it follows you around. 

Lastly we have the button Close All Nodes, which halts all movement of the robot and nodes that were launched through the GUI. It is important to note that the user should close all nodes in between running follow mode and circle drive so they do not operate simultaneously. Furthermore, the user should run close all nodes before closing the GUI to ensure all the nodes close cleanly.

