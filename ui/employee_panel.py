from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from db import db


class EmployeePanel(QWidget):

    def __init__(self, user):
        super().__init__()

        self.emp = user["data"]

        self.setWindowTitle("Employee Panel")
        self.setGeometry(300, 200, 600, 450)

        # MAIN LAYOUT
        layout = QVBoxLayout()

        # ─────────────────────────
        # TITLE
        # ─────────────────────────
        title = QLabel(f"Welcome {self.emp['full_name']} Worker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        """)

        layout.addWidget(title)

        # ─────────────────────────
        # TASK LIST CONTAINER
        # ─────────────────────────
        self.task_box = QVBoxLayout()

        self.task_group = QGroupBox("Assigned Tasks")
        self.task_group.setLayout(self.task_box)

        layout.addWidget(self.task_group)

        # ─────────────────────────
        # BUTTON
        # ─────────────────────────
        self.btn = QPushButton("Mark Selected Task Completed")
        self.btn.clicked.connect(self.complete_task)

        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        layout.addWidget(self.btn)

        self.setLayout(layout)

        # LOAD TASKS
        self.load_tasks()

    # ─────────────────────────────
    # LOAD TASKS (UI STYLE)
    # ─────────────────────────────
    def load_tasks(self):

        # CLEAR OLD UI
        for i in reversed(range(self.task_box.count())):
            widget = self.task_box.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        tasks = db.get_tasks({
            "assigned_to": self.emp["emp_id"]
        })

        self.task_buttons = []

        for t in tasks:

            text = f"{t['task_id']} - {t['title']} - {t['status']}"

            btn = QRadioButton(text)

            btn.setStyleSheet("""
                QRadioButton {
                    font-size: 14px;
                    padding: 6px;
                }
            """)

            self.task_box.addWidget(btn)

            self.task_buttons.append((btn, t["task_id"]))

    # ─────────────────────────────
    # COMPLETE TASK
    # ─────────────────────────────
    def complete_task(self):

        selected_id = None

        for btn, tid in self.task_buttons:

            if btn.isChecked():
                selected_id = tid
                break

        if not selected_id:

            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a task first"
            )

            return

        db.update_task_status(
            selected_id,
            "Completed"
        )

        QMessageBox.information(
            self,
            "Done",
            "Task marked as completed"
        )

        self.load_tasks()