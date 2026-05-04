from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('clearpath_nav2_demos'), 'launch', 'slam.launch.py')
        ]),
        launch_arguments={'log_level': 'warn'}.items()
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('clearpath_viz'), 'launch', 'view_navigation.launch.py')
        ]),
        launch_arguments={'namespace': 'j100_0000'}.items()
    )

    ros2 launch clearpath_viz view_navigation.launch.py namespace:=j100_0000
    
    return LaunchDescription([

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
        
        slam_launch,
        rviz_launch

    ])
