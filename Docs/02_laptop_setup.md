# Laptop Setup

The laptop runs the GUI locally and SSHes into the robot to launch nodes. All necessary files are included in the repository — outside of adding your computer's username in a few places, you do not need to write any files yourself.

## 1. Install ROS 2 Jazzy

Follow the official ROS 2 Jazzy installation instructions for Ubuntu:
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

## 2. Clearpath Offboard Computer Setup

Follow Clearpath's offboard computer setup guide to configure your laptop to communicate with the robot:
https://docs.clearpathrobotics.com/docs/ros/installation/offboard_pc/

This will generate a `~/clearpath/` directory on your laptop containing a `setup.bash` file with the network configuration needed to connect to the robot's ROS graph.

> **Important:** Your `~/clearpath/setup.bash` must contain the correct `ROS_DISCOVERY_SERVER` IP address for your robot. Verify this matches your robot's actual IP address before proceeding.

## 3. Install Dependencies

```bash
sudo apt install sshpass
sudo apt install gnome-terminal
sudo apt install python3-pyqt5
```

## 4. Clone the Repository

```bash
cd ~
git clone -b kate_dev https://github.com/kate-whitmire/hold_my_gear_jackal.git
cd hold_my_gear_jackal
```

## 5. Build the Workspace

```bash
colcon build --symlink-install
```

## 6. Update the Robot IP Address

Open `src/jackal_yolo_follow/jackal_yolo_follow/follow_mode_gui.py` and update the robot IP address to match your robot:

```python
# Find and replace all instances of:
robot@10.10.0.7
# with:
robot@<your_robot_ip>
```

## 7. Set Up the Workspace setup.bash

The repo includes `setup.bash` and `robot.yaml` at the root level. Before running the demo, update both files with your specific network information.

In `setup.bash`, update the `ROS_DISCOVERY_SERVER` to match your robot's IP:
```bash
export ROS_DISCOVERY_SERVER=":11811;127.0.0.1:11811;:11811;"
```

In `robot.yaml`, update `hosts:` to include your computer's name and ip.


## 8. Set Up the Desktop Launcher

The repo includes `JackalDemo.desktop` at the root level. Copy it to your Desktop:

```bash
cp ~/hold_my_gear_jackal/JackalDemo.desktop ~/Desktop/
```

Make it executable:

```bash
chmod +x ~/Desktop/JackalDemo.desktop
```

Open `~/Desktop/JackalDemo.desktop` and update the username to match yours:

```ini
[Desktop Entry]
Name=Jackal Demo
Exec=/home/<your_username>/Desktop/run_demo.sh
Icon=/home/<your_username>/Desktop/Jackal Image.png
Terminal=false
Type=Application
```

Right-click the `.desktop` file and select **Allow Launching**.

## What the Laptop Side Does

- Runs the PyQt5 GUI locally
- SSHes into the robot to launch ROS nodes when buttons are clicked
- Runs RViz locally for visualization
- Uses `~/clearpath/setup.bash` to configure the ROS network and connect to the robot's ROS graph
