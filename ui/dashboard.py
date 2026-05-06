from PyQt6.QtWidgets import *


class Dashboard(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Smart City Dashboard")
        self.setGeometry(300, 150, 800, 500)

        layout = QVBoxLayout()

        # ───── TITLE ─────
        title = QLabel(f"Welcome, {user['data']['full_name']}")
        title.setStyleSheet("font-size:18px;font-weight:bold;")

        layout.addWidget(title)

        # ───── ROLE LOGIC ─────
        role = user["data"]["role"]

        if role == "admin":
            from ui.admin_panel import AdminPanel
            self.panel = AdminPanel(user)

        else:
            from ui.employee_panel import EmployeePanel
            self.panel = EmployeePanel(user)

        # IMPORTANT: embed panel, not separate window
        layout.addWidget(self.panel)

        self.setLayout(layout)