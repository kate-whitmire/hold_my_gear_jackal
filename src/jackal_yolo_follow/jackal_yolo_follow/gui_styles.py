from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt

STYLESHEET = """
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
"""

class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Connection")
        self.setStyleSheet(STYLESHEET)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)

        label = QLabel("Enter robot password:")
        label.setStyleSheet("font-size: 18px; font-weight: normal;")
        layout.addWidget(label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        btn = QPushButton("Connect")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_password(self):
        return self.password_input.text()


def create_main_widget(button_callbacks):
    w = QWidget()
    w.setWindowTitle("Jackal Demo")
    w.setStyleSheet(STYLESHEET)

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
    button1.clicked.connect(button_callbacks['yolo_follower'])
    layout.addWidget(button1)

    button2 = QPushButton('Start: Drive in Circle')
    button2.clicked.connect(button_callbacks['circle_drive'])
    layout.addWidget(button2)

    button3 = QPushButton('Open Rviz')
    button3.clicked.connect(button_callbacks['open_rviz'])
    layout.addWidget(button3)

    b = QPushButton('Close All Nodes')
    b.setObjectName("danger")
    b.clicked.connect(button_callbacks['close_all'])
    layout.addWidget(b)

    w.setLayout(layout)
    # w.resize(300, 200)
    return w