from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')
        ])
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('clearpath_nav2_demos'), 'launch', 'nav2.launch.py')
        ])
    )

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('clearpath_nav2_demos'), 'launch', 'slam.launch.py')
        ])
    )
    
    return LaunchDescription([
        realsense_launch,
        nav2_launch,
        slam_launch,

        Node(
            package='depthimage_to_laserscan',
            namespace='j100_0000',
            executable='depthimage_to_laserscan_node',
            name='sim', # ??
            ros_arguments=['-r depth:=/camera/camera/depth/image_rect_raw', 
                           '-r depth_camera_info:=/camera/camera/depth/camera_info',
                           '-r scan:=/j100_0000/sensors/lidar2d_0/scan',
                           '-p range_min:=0.3',
                           '-p range_max:=5.0',
                           '-p output_frame:=base_link']
        ),

        ExecuteProcess(
            cmd=['xterm', '-e', 'bash -c "export PYTHONPATH=/home/robot/vision_venv/lib/python3.12/site-packages:$PYTHONPATH &&'
            'source ~/vision_venv/bin/activate && '
            'ros2 run jackal_yolo_follow yolo_follower; bash"'],
            output = 'screen'
        ),

        Node(
            package='jackal_yolo_follow',
            namespace='j100_0000', # ??
            executable='nav_to_pose_test',
            name='sim', # ??
        )   

    ])
