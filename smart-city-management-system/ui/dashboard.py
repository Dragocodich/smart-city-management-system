from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Dashboard(QWidget):

    def __init__(self, user, on_logout=None):
        super().__init__()

        self.user = user
        self.on_logout = on_logout

        self.setWindowTitle("Smart City Management System - Dashboard")
        self.setGeometry(100, 50, 1200, 800)
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # ─────────────────────────────
        # HEADER BANNER
        # ─────────────────────────────
        header = QWidget()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("🏙️ Smart City Management System")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")

        full_name = user.get('data', {}).get('full_name', 'User')
        subtitle = QLabel(f"Welcome back, {full_name}!")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9);")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header.setLayout(header_layout)

        layout.addWidget(header)

        # ─────────────────────────────
        # CONTENT AREA
        # ─────────────────────────────
        content = QWidget()
        content.setStyleSheet("background-color: #f5f7fa;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 30, 30, 30)

        # ROLE-BASED PANEL
        if user["type"] == "citizen":
            from ui.citizen_panel import CitizenPanel
            self.panel = CitizenPanel(user, self.handle_logout)
        else:
            role = user["data"].get("role", "")
            if role == "admin":
                from ui.admin_panel import AdminPanel
                self.panel = AdminPanel(user, self.handle_logout)
            else:
                from ui.employee_panel import EmployeePanel
                self.panel = EmployeePanel(user, self.handle_logout)

        # Adjust panel styling
        self.panel.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border: 1px solid #ecf0f1;
        """)

        content_layout.addWidget(self.panel)
        content.setLayout(content_layout)

        layout.addWidget(content)

        self.setLayout(layout)

    def handle_logout(self):
        """Handle logout from any panel"""
        if self.on_logout:
            self.on_logout()
        self.close()