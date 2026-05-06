from PyQt6.QtWidgets import *
from db import db


class LoginWindow(QWidget):
    def __init__(self, role):
        super().__init__()

        self.role = role

        self.setWindowTitle(f"Smart City Login - {role}")
        self.setGeometry(400, 200, 300, 200)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn = QPushButton("Login")
        self.btn.clicked.connect(self.login)

        self.status = QLabel("")

        layout.addWidget(QLabel(f"Role: {role.upper()}"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.btn)
        layout.addWidget(self.status)

        self.setLayout(layout)

    def login(self):
        user = db.authenticate_user(
            self.username.text().strip(),
            self.password.text().strip()
        )

        if user:
            # optional role check (IMPORTANT)
            if user["data"]["role"] != self.role:
                self.status.setText("❌ Wrong role login")
                return

            self.status.setText("Login successful")
            self.open_dashboard(user)
        else:
            self.status.setText("Invalid credentials")

    def open_dashboard(self, user):
        from ui.dashboard import Dashboard
        self.dashboard = Dashboard(user)
        self.dashboard.show()
        self.close()