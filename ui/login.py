from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from db import db


class LoginWindow(QWidget):

    def __init__(self, role):
        super().__init__()

        # SAVE ROLE
        self.role = role

        # WINDOW SETTINGS
        self.setWindowTitle(f"{role.capitalize()} Login")
        self.setGeometry(500, 250, 350, 250)

        # MAIN LAYOUT
        layout = QVBoxLayout()

        # TITLE
        title = QLabel(f"{role.capitalize()} Portal")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # USERNAME
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        self.username.setMinimumHeight(40)

        # PASSWORD
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setMinimumHeight(40)

        # LOGIN BUTTON
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(40)

        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.login_btn.clicked.connect(self.login)

        # STATUS LABEL
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ADD WIDGETS
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.status)

        self.setLayout(layout)

    # ─────────────────────────────
    # LOGIN FUNCTION
    # ─────────────────────────────
    def login(self):

        username = self.username.text().strip()
        password = self.password.text().strip()

        # EMPTY CHECK
        if not username or not password:

            self.status.setText("⚠ Please fill all fields")
            return

        # AUTHENTICATE USER
        user = db.authenticate_user(
            username,
            password,
            self.role
        )

        # SUCCESS
        if user:

            self.status.setText("✅ Login successful")

            self.open_dashboard(user)

        # FAILED
        else:

            self.status.setText("❌ Invalid credentials")

    # ─────────────────────────────
    # OPEN DASHBOARD
    # ─────────────────────────────
    def open_dashboard(self, user):

        from ui.dashboard import Dashboard

        self.dashboard = Dashboard(user)

        self.dashboard.show()

        self.close()