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

        TimerAction(
            period = 3.0,
            actions = [
                Node(
                    package='depthimage_to_laserscan',
                    namespace='j100_0000',
                    executable='depthimage_to_laserscan_node',
                    name='sim', # ??
                    remappings = [
                        ('depth', '/camera/camera/depth/image_rect_raw'),
                        ('depth_camera_info', '/camera/camera/depth/camera_info'),
                        ('scan', '/j100_0000/sensors/lidar2d_0/scan'),
                    ],
                    parameters = [{
                        'range_min': 0.3,
                        'range_max': 5.0,
                        'output_frame': 'base_link'
                    }]
                )
            ]
        ),

        ExecuteProcess(
            cmd=['bash', '-c', # took out 'xterm', '-e', from the beginning of line
                'source ~/vision_venv/bin/activate && '                
                'export PYTHONPATH=/home/robot/vision_venv/lib/python3.12/site-packages:$PYTHONPATH &&'
                'ros2 run jackal_yolo_follow yolo_follower'],
            output = 'screen'
        )

    ])
