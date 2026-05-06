from PyQt6.QtWidgets import *
from db import get_tasks, update_task_status

class EmployeePanel(QWidget):
    def __init__(self, user):
        super().__init__()
        self.emp = user["data"]

        self.setWindowTitle("Employee Panel")
        self.setGeometry(300, 200, 500, 400)

        layout = QVBoxLayout()

        self.list = QListWidget()
        self.load_tasks()

        btn = QPushButton("Mark Completed")
        btn.clicked.connect(self.complete_task)

        layout.addWidget(self.list)
        layout.addWidget(btn)

        self.setLayout(layout)

    def load_tasks(self):
        tasks = get_tasks({"assigned_to": self.emp["emp_id"]})
        for t in tasks:
            self.list.addItem(
                f"{t['task_id']} - {t['title']} - {t['status']}"
            )

    def complete_task(self):
        item = self.list.currentItem()
        if item:
            tid = int(item.text().split()[0])
            update_task_status(tid, "Completed")
            QMessageBox.information(self, "Done", "Task Completed")