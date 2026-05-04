# Robot Setup

The robot runs all ROS nodes for the demo. The relevant workspace on the robot is `~/clearpath_ws`, which contains the `jackal_yolo_follow` package cloned from this repository.

## 1. Base System Assumptions

The Jackal image is assumed to provide:

- ROS 2 Jazzy
- Clearpath platform services
- Nav2 and SLAM Toolbox
- A workspace at `~/clearpath_ws`

If your image differs, adapt the paths accordingly.


## 2. Install ROS 2 Jazzy

Follow the official ROS 2 Jazzy installation for Ubuntu:
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

## 3. Install ROS Dependencies

```bash
sudo apt install ros-jazzy-realsense2-camera
sudo apt install ros-jazzy-depthimage-to-laserscan
sudo apt install ros-jazzy-slam-toolbox
```

Install Clearpath packages:

```bash
wget https://packages.clearpathrobotics.com/public.key -O - | sudo apt-key add -
sudo sh -c 'echo \
    "deb https://packages.clearpathrobotics.com/stable/ubuntu $(lsb_release -cs) main" > \
    /etc/apt/sources.list.d/clearpath-latest.list'
sudo apt-get update

sudo wget \
    https://raw.githubusercontent.com/clearpathrobotics/public-rosdistro/master/rosdep/50-clearpath.list \
    -O /etc/ros/rosdep/sources.list.d/50-clearpath.list
rosdep update
```

## 4. Clone the Repository

```bash
cd ~
git clone -b kate_dev https://github.com/kate-whitmire/hold_my_gear_jackal.git clearpath_ws
cd clearpath_ws
```

## 5. Set Up the Python Virtual Environment

The YOLO model runs inside a virtual environment to avoid conflicts with the system Python packages used by ROS 2:

```bash
python3 -m venv ~/vision_venv
source ~/vision_venv/bin/activate
pip install ultralytics
pip install opencv-python
deactivate
```

Download the YOLO model to the robot's home directory:

```bash
wget -O ~/yolo11n.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
```

## 6. Build the Workspace

```bash
cd ~/clearpath_ws
colcon build
source install/setup.bash
```

## 7. Configure sudoers for Clean Shutdown

The laptop GUI sends a kill command for the RealSense process on shutdown. This requires sudo without a password prompt. Add the following:

```bash
sudo visudo
```

Add this line at the bottom of the file:

```
robot ALL=(ALL) NOPASSWD: /usr/bin/pkill
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X` in nano).

## 8. Verify the Setup

Test the launch file directly from an SSH session on the robot:

```bash
source /etc/clearpath/setup.bash
source ~/clearpath_ws/install/setup.bash
ros2 launch jackal_yolo_follow regular_follow_mode_launch.py
```

You should see the RealSense initialize and `[INFO] [yolo_person_follower]: Follow Active` appear in the output after a few seconds. The robot should detect and follow a person who walks in front of the camera.
