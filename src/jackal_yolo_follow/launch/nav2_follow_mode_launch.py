from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='realsense2_camera',
            namespace='j100_0000', # ??
            executable='rs_launch.py',
            name='sim', # ??
            # arguments=['--ros-args', '--log-level', 'info']
        ),
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
            # arguments=['--ros-args', '--log-level', 'info']

        ),
        Node(
            package='clearpath_nav2_demos',
            namespace='j100_0000', # ??
            executable='slam.launch.py.py',
            name='sim', # ??
        ),
        Node(
            package='clearpath_nav2_demos',
            namespace='j100_0000', # ??
            executable='nav2.launch.py.py',
            name='sim', # ??
        )        


        # Node(
        #     package='turtlesim',
        #     executable='mimic',
        #     name='mimic',
        #     remappings=[
        #         ('/input/pose', '/turtlesim1/turtle1/pose'),
        #         ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
        #     ]
        # )
    ])
