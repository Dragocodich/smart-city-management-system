from PyQt6.QtWidgets import *
from db import db


class AdminPanel(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()

        self.load_complaints()

        btn = QPushButton("Assign Task")
        btn.clicked.connect(self.assign_task_to_employee)

        layout.addWidget(self.list_widget)
        layout.addWidget(btn)

        self.setLayout(layout)

    # ───── LOAD COMPLAINTS ─────
    def load_complaints(self):
        self.list_widget.clear()

        complaints = db.get_complaints()

        for c in complaints:
            self.list_widget.addItem(
                f"{c[0]} - {c[1]} - {c[2]}"
            )

    # ───── ASSIGN TASK ─────
    def assign_task_to_employee(self):
        item = self.list_widget.currentItem()

        if not item:
            QMessageBox.warning(self, "Error", "Please select a complaint")
            return

        cid = int(item.text().split(" - ")[0])

        # Example assignment (you can later make dynamic UI)
        db.assign_task(
            complaint_id=cid,
            dept_id=1,
            assigned_to=2,
            assigned_by=self.user["data"]["emp_id"],
            title="Fix reported issue",
            priority="High",
            due_date=None
        )

        QMessageBox.information(self, "Success", "Task Assigned Successfully")