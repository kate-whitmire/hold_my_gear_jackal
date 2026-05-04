import sys, os, signal, subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from jackal_yolo_follow.gui_styles import STYLESHEET, PasswordDialog, create_main_widget

password = None

class DemoWidget(QWidget):
    def closeEvent(self, event):
        close_all_nodes()
        event.accept()

procs = {}

# Strings for each launch/run command to be used in start()
CMDS = { 
    'yolo_follower': ['ros2', 'launch', 'jackal_yolo_follow', 'regular_follow_mode_launch.py'],
    
    'circle_drive': ['ros2', 'run', 'jackal_yolo_follow', 'circle_drive'],

    'open_rviz' : ['ros2', 'launch', 'clearpath_nav2_demos', 'slam.launch.py']

}

NODE_NAMES = ['yolo_follower', 'circle_drive', 'open_rviz']

def start(name, password):
    # start() opens a new terminal, SSH's into the robot, and runs command
    p = procs.get(name)
    if p and p.poll() is None:
        return
    cmd_str = ' '.join(CMDS[name])
    procs[name] = subprocess.Popen([
        'gnome-terminal', '--',
        'bash', '-c',
        f'sshpass -p {password} ssh robot@10.10.0.7 '
        # f'"source ~/.bashrc && ' # CANNOT source bashrc bc it's a non-interactive terminal
        f'"export ROS_DOMAIN_ID=0 && '
        f'source /etc/clearpath/setup.bash && '
        f'source /opt/ros/jazzy/setup.bash && '
        f'source ~/clearpath_ws/install/setup.bash && '
        f'{cmd_str}; exec bash"'
    ])

def open_rviz():
    # Launches SLAM from CMDS on robot then runs rviz manually on computer
    # SLAM launch spins up ros_launch_xxxx nodes that can't be shut down by close all nodes
        # Best solution is to restart robot if they pile up in background
    start('open_rviz', password)
    subprocess.Popen([
        'gnome-terminal', '--',
        'bash', '-c',
        'source ~/hold_my_gear_jackal/setup.bash && '
        'ros2 launch clearpath_viz view_navigation.launch.py namespace:=j100_0000; exec bash'
    ])

def close_all_nodes():
    print('Closing all nodes...')

    # Hard kills every node
    if password:
        subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', 'pkill -9 -f yolo_follower'])
        subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', 'pkill -9 -f slam_toolbox'])
        subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', 'pkill -9 -f launch_ros'])
        subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', 'pkill -9 -f realsense'])
        subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', 'pkill -9 -f circle_drive'])

    # Kills any terminals opened by launch files
    subprocess.run(['pkill', '-f', 'gnome-terminal'])


def main():
    app = QApplication(sys.argv)
    global password

    while True:
        # Pulls up password sign-in window
        dialog = PasswordDialog()
        if dialog.exec_() != QDialog.Accepted:
            sys.exit()
        password = dialog.get_password()

        # Checks if password is correct, retry if failed
        result = subprocess.run(
            ['sshpass', '-p', password, 'ssh',
             '-o', 'ConnectTimeout=5',
             '-o', 'StrictHostKeyChecking=no',
             'robot@10.10.0.7', 'echo connected'],
            capture_output=True
        )

        if result.returncode == 0:
            break
        else:
            QMessageBox.warning(None, 'Connection Failed', 'Wrong password or could not connect. Try again.')

    # Buttons for the GUI
    w = create_main_widget({
        'yolo_follower': lambda: start('yolo_follower', password),
        'circle_drive': lambda: start('circle_drive', password),
        'open_rviz' : lambda: open_rviz(),
        'close_all': close_all_nodes
    })

    # Center & resize the GUI on the screen
    w.resize(400, 300)
    center = QApplication.primaryScreen().geometry().center()
    w.move(center - w.rect().center())
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    
