from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ui.login import LoginWindow


class RoleSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart City Portal - Role Selection")
        self.setGeometry(350, 150, 500, 400)
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # TITLE
        title = QLabel("Select Login Type")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # SUBTITLE
        subtitle = QLabel("Choose your role to continue")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # SEPARATOR
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #ecf0f1;")

        # BUTTONS
        btn_admin = QPushButton("👨‍💼 Login as Admin")
        btn_admin.setMinimumHeight(60)
        btn_admin.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        btn_admin.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_admin.setStyleSheet(self._get_button_style("#e74c3c"))

        btn_employee = QPushButton("👨‍💻 Login as Employee")
        btn_employee.setMinimumHeight(60)
        btn_employee.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        btn_employee.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_employee.setStyleSheet(self._get_button_style("#3498db"))

        btn_citizen = QPushButton("👤 Login as Citizen")
        btn_citizen.setMinimumHeight(60)
        btn_citizen.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        btn_citizen.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_citizen.setStyleSheet(self._get_button_style("#27ae60"))

        btn_admin.clicked.connect(lambda: self.open_login("admin"))
        btn_employee.clicked.connect(lambda: self.open_login("employee"))
        btn_citizen.clicked.connect(lambda: self.open_login("citizen"))

        # ADD TO LAYOUT
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(line)
        layout.addSpacing(10)
        layout.addWidget(btn_admin)
        layout.addWidget(btn_employee)
        layout.addWidget(btn_citizen)
        layout.addStretch()

        self.setLayout(layout)
        self.login = None

    def _get_button_style(self, color):
        """Generate button stylesheet with gradient"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {self._darken_color(color)});
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self._darken_color(color)}, stop:1 {self._darken_color(color, 2)});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self._darken_color(color, 2)}, stop:1 {self._darken_color(color, 3)});
            }}
        """

    def _darken_color(self, color, factor=1):
        """Darken hex color"""
        color_map = {
            "#e74c3c": ["#c0392b", "#a93226", "#922b21"],
            "#3498db": ["#2980b9", "#1f618d", "#154360"],
            "#27ae60": ["#1e8449", "#186a3b", "#145a32"]
        }
        return color_map.get(color, [color, color, color])[factor - 1] if factor > 0 else color

    def open_login(self, role):
        self.login = LoginWindow(role, self)
        self.login.show()
        self.hide()