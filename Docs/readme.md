# Hold My Gear — Jackal Person Following Demo

A person-following demo for the Clearpath Robotics Jackal using a RealSense D435 depth camera and YOLO object detection. The demo is operated from a laptop via a simple GUI — no terminal knowledge required for the end user. The robot setup is already completed for use on the NRG Jackal at UT Austin.

![Jackal Demo](Jackal%20Image.png)

## What It Does

- **Follow Mode** — The robot detects and follows the closest person in view using YOLO and depth-based distance estimation
- **Circle Drive** — The robot spins in place
- **RViz** — Optional live map view using SLAM Toolbox

## Quick Start

1. Set up the robot (`clearpath_ws`) → see [Robot Setup](03_robot_setup.md)
2. Set up your laptop (`hold_my_gear_jackal`) → see [Laptop Setup](02_laptop_setup.md)
3. Double-click the **Jackal Demo** desktop icon, enter the robot password, and go

## Documentation

| Doc | Description |
|-----|-------------|
| [01 — Overview](01_overview.md) | Repo layout, system overview, and how it works |
| [02 — Laptop Setup](02_laptop_setup.md) | Setting up the offboard operator computer |
| [03 — Robot Setup](03_robot_setup.md) | Setting up the Jackal's onboard computer |

## Requirements

- Clearpath Robotics Jackal
- Intel RealSense D435
- ROS 2 Jazzy
- Ubuntu 24
- Python 3.12
