import sys
from PyQt6.QtWidgets import QApplication

from db import db
from ui.role_selector import RoleSelector


app = QApplication(sys.argv)

db.connect()

window = RoleSelector()
window.show()

sys.exit(app.exec())