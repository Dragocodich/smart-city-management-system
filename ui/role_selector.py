from PyQt6.QtWidgets import *
from ui.login import LoginWindow


class RoleSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart City Portal")
        self.setGeometry(400, 200, 300, 200)

        layout = QVBoxLayout()

        title = QLabel("Select Login Type")
        title.setStyleSheet("font-size:16px;font-weight:bold;")
        layout.addWidget(title)

        btn_admin = QPushButton("Login as Admin")
        btn_employee = QPushButton("Login as Employee")
        btn_citizen = QPushButton("Login as Citizen")

        btn_admin.clicked.connect(lambda: self.open_login("admin"))
        btn_employee.clicked.connect(lambda: self.open_login("employee"))
        btn_citizen.clicked.connect(lambda: self.open_login("citizen"))

        layout.addWidget(btn_admin)
        layout.addWidget(btn_employee)
        layout.addWidget(btn_citizen)

        self.setLayout(layout)

    def open_login(self, role):
        self.login = LoginWindow(role)
        self.login.show()
        self.close()