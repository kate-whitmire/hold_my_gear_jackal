from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')
        ]),
        launch_arguments={'log_level': 'warn'}.items()
    )

    return LaunchDescription([
        realsense_launch,

        ExecuteProcess(
            cmd=['bash', '-c', # took out 'xterm', '-e', from the beginning of line
                'source ~/vision_venv/bin/activate && '                
                'export PYTHONPATH=/home/robot/vision_venv/lib/python3.12/site-packages:$PYTHONPATH &&'
                'ros2 run jackal_yolo_follow yolo_follower'],
            output = 'screen'
        )

    ])
