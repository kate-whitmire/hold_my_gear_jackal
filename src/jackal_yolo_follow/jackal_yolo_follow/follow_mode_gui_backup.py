import sys, os, signal, subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

password = None

class DemoWidget(QWidget):
    def closeEvent(self, event):
        close_all_nodes()
        event.accept()

procs = {}

CMDS = { 
    'yolo_follower': ['ros2', 'launch', 'jackal_yolo_follow', 'regular_follow_mode_launch.py'],
    
    'circle_drive' : ['ros2', 'topic', 'pub', '--once', '/j100_0000/cmd_vel', 'geometry_msgs/msg/TwistStamped', '"{linear: {x: 0.5}, angular: {z: 0.0}}"']
    # Now I have to write an executable to make the robot drive in a circle
    # *Face palm*

}

NODE_NAMES = ['yolo_follower', 'circle_drive']


# def start(name): # removed password to correspond with calls below
#     p = procs.get(name)
#     if p and p.poll() is None:
#         return
#     cmd_str = ' '.join(CMDS[name])
   
#     procs[name] = subprocess.Popen([
#         'gnome-terminal', '--',
#         'bash', '-c',
#         # f'sshpass -p {password} ssh robot@10.10.0.7'
#         f'source /opt/ros/jazzy/setup.bash && '
#         f'source ~/hold_my_gear_jackal/install/setup.bash && '
#         f'{cmd_str}; exec bash'        
#     ])

def start(name, password):
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
        # f'sudo pkill -9 -f realsense' want to see if I can incorporate this here
        f'{cmd_str}; exec bash"'
    ])

## Literally doesn't do anything anymore lol
# def stop(name):
#     p = procs.get(name)
#     if not p:
#         return
#     try:
#         os.killpg(os.getpgid(p.pid), signal.SIGKILL)
#         try:
#             p.wait(timeout=2)
#         except subprocess.TimeoutExpired:
#             os.killpg(os.getpgid(p.pid), signal.SIGKILL)
#     except Exception:
#         pass
#     procs.pop(name, None)


def close_all_nodes():
    print('Closing all nodes...')
    # for n in NODE_NAMES:
    #     stop(n)

    # Kill lingering ROS nodes
    if password:
        print('SSHing into robot to kill processes...')
        subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', 'pkill -9 -f yolo_follower'])
        subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', f'sudo -S pkill -9 -f realsense'], input=password.encode())
    subprocess.run(['pkill', '-f', 'gnome-terminal'])


    #     print('SSHing into robot to kill processes...')
    #     result = subprocess.run(['sshpass', '-p', password,
    #         'ssh', 'robot@10.10.0.7',
    #         f'echo {password} | sudo -S pkill -9 -f yolo_follower; '
    #         f'sleep 1; '
    #         f'echo {password} | sudo -S pkill -9 -f realsense; '
    #         f'sleep 1; '
    #         f'pkill -9 -f ros2']) # This kills all other ros nodes running in the background (theoretically)
    #     print(f'SSH result: {result.returncode}')
    # subprocess.run(['pkill', '-f', 'gnome-terminal'])

        # if password:
        #     print('SSHing into robot to kill processes...')
        #     subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', 'pkill -9 -f yolo_follower'])
        #     subprocess.run(['sshpass', '-p', password, 'ssh', 'robot@10.10.0.7', f'sudo -S pkill -9 -f realsense'], input=password.encode())
        # subprocess.run(['pkill', '-f', 'gnome-terminal'])



def main():

# Also an option to add function stop_all_nodes for gazebo or anything 
# running in the background, could be relevant I guess if we want to pull up rviz. 
# Actually I do want rviz.

    app = QApplication(sys.argv)
    global password

    # Ask for password when GUI opens
    while True:
        password, ok = QInputDialog.getText(
            None,
            'Robot Connection',
            'Enter robot password:',
            QLineEdit.Password
        )
        if not ok:
            sys.exit()

        # Check if password is correct
        result = subprocess.run([
            'sshpass', '-p', password, 'ssh', '-o', 'ConnectTimeout=5',
             '-o', 'StrictHostKeyChecking=no', 'robot@10.10.0.7', 'echo connected'
        ])
        if result.returncode == 0:
            break # password is correct
        else:
            QMessageBox.warning(None, 'Connection Failed', 'Wrong password or could not connect, please try again.')

    # subprocess.Popen([
        # Adds a terminal on sign-in
        # 'gnome-terminal', '--',
        # 'bash', '-c',
        # f'sshpass -p {password} ssh robot@10.10.0.7'
    # ])

    w = DemoWidget()
    w.setWindowTitle("Jackal Demo")
    w.setStyleSheet("""
        QWidget {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2
            );
        }
        QLabel {
            color: white;
            font-size: 20px;
            font-weight: bold;
        }
        QLabel#subtitle {
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
            font-weight: normal;
        }
        QPushButton {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 14px;
            text-align: center;
        }
        QPushButton:hover {
            background: rgba(255, 255, 255, 0.35);
        }
        QPushButton:pressed {
            background: rgba(255, 255, 255, 0.15);
        }
        QPushButton#danger {
            background: rgba(255, 100, 100, 0.3);
        }
        QPushButton#danger:hover {
            background: rgba(255, 100, 100, 0.5);
        }
    """)

    layout = QVBoxLayout(w)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(8)

    title = QLabel("Jackal Demo")
    subtitle = QLabel("UGV Control Panel")
    subtitle.setObjectName("subtitle")
    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addSpacing(8)

    button1 = QPushButton('Start: Follow Mode')
    button1.clicked.connect(lambda: start('yolo_follower', password)) # took out password at end
    layout.addWidget(button1)

    button2 = QPushButton('Start: Drive in Circle')
    button2.clicked.connect(lambda: start('circle_drive', password))
    layout.addWidget(button2)

    b = QPushButton('Close All Nodes')
    b.setObjectName("danger")
    b.clicked.connect(close_all_nodes)
    layout.addWidget(b)

    w.setLayout(layout)
    w.resize(300, 200)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
