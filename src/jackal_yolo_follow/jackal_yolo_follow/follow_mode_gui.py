import sys, os, signal, subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt

procs = {}

CMDS = { 
    'yolo_follower': ['ros2', 'launch', 'jackal_yolo_follow', 'regular_follow_mode_launch.py'],
    
    'circle_drive' : []
    # Now I have to write an executable to make the robot drive in a circle
    # *Face palm*

}

NODE_NAMES = ['yolo_follower', 'circle_drive']


def start(name, password):
    p = procs.get(name)
    if p and p.poll() is None:
        return
    cmd_str = ' '.join(CMDS[name])
    procs[name] = subprocess.Popen([
        'gnome-terminal', '--',
        'bash', '-c',
        f'sshpass -p {password} ssh robot@10.10.0.7'
        f'source /opt/ros/jazzy/setup.bash && '
        f'source ~/hold_my_gear_jackal/install/setup.bash && '
        f'{cmd_str}; exec bash'        
    ])


def stop(name):
    p = procs.get(name)
    if not p:
        return
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        try:
            p.wait(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
    except Exception:
        pass
    procs.pop(name, None)


def close_all_nodes():
    for n in NODE_NAMES:
        stop(n)


def main():

# Also an option to add function stop_all_nodes for gazebo or anything 
# running in the background, could be relevant I guess if we want to pull up rviz. 
# Actually I do want rviz.
# Actually I think yolo_follower already pulls up rviz. Have to verify.

    app = QApplication(sys.argv)

    # Ask for password when GUI opens
    password, ok = QInputDialog.getText(
        None,
        'Robot Connection',
        'Enter robot password:',
        QLineEdit.Password
    )
    if not ok:
        sys.exit()

    w = QWidget()
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
    button1.clicked.connect(lambda: start('yolo_follower'))
    layout.addWidget(button1)

    button2 = QPushButton('Start: Drive in Circle')
    button2.clicked.connect(lambda: start('circle_drive'))
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
    
