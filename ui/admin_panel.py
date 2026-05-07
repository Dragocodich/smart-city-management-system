from PyQt6.QtWidgets import *
from db import db


class AdminPanel(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Admin Control Panel")
        self.setGeometry(300, 150, 750, 500)

        # ─────────────────────────────
        # MAIN LAYOUT
        # ─────────────────────────────
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        # ─────────────────────────────
        # CLEAN ROLE FIX (NO DUPLICATION)
        # ─────────────────────────────
        raw_role = self.user['data']['role']

        # prevent DB/string duplication bug
        clean_role = raw_role.replace(
            "System Administrator System Administrator",
            "System Administrator"
        ).strip()

        # also handle repeated "Welcome" issues
        clean_role = clean_role.replace("Welcome", "").strip()

        # ─────────────────────────────
        # SINGLE WELCOME LABEL (FIXED)
        # ─────────────────────────────
        self.title_label = QLabel(f"Welcome, {clean_role}")

        self.title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 20px;
        """)

        self.layout_main.addWidget(self.title_label)

        # ─────────────────────────────
        # BUTTONS
        # ─────────────────────────────
        self.btn_complaints = QPushButton("Manage Complaints")
        self.btn_tasks = QPushButton("Assign Tasks")
        self.btn_employees = QPushButton("Manage Employees")
        self.btn_analytics = QPushButton("Analytics Dashboard")

        self.layout_main.addWidget(self.btn_complaints)
        self.layout_main.addWidget(self.btn_tasks)
        self.layout_main.addWidget(self.btn_employees)
        self.layout_main.addWidget(self.btn_analytics)

        # ─────────────────────────────
        # SIGNALS
        # ─────────────────────────────
        self.btn_complaints.clicked.connect(self.open_complaints)
        self.btn_tasks.clicked.connect(self.open_task_assigner)
        self.btn_employees.clicked.connect(self.open_employees)
        self.btn_analytics.clicked.connect(self.open_analytics)

        # ─────────────────────────────
        # WINDOW CACHE (PREVENT DUPLICATES)
        # ─────────────────────────────
        self.windows = {}

    # ─────────────────────────────
    # COMPLAINTS WINDOW
    # ─────────────────────────────
    def open_complaints(self):

        if "complaints" in self.windows:
            self.windows["complaints"].raise_()
            self.windows["complaints"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Complaints")

        layout = QVBoxLayout()
        list_widget = QListWidget()

        try:
            db.cursor.execute("""
                SELECT complaint_id, title, status
                FROM complaints
                ORDER BY complaint_id DESC
            """)

            for row in db.cursor.fetchall():
                list_widget.addItem(f"{row[0]} - {row[1]} - {row[2]}")

        except Exception as e:
            print("❌ Complaint load error:", e)

        layout.addWidget(list_widget)
        win.setLayout(layout)

        self.windows["complaints"] = win
        win.show()

    # ─────────────────────────────
    # TASK ASSIGNER
    # ─────────────────────────────
    def open_task_assigner(self):

        if "tasks" in self.windows:
            self.windows["tasks"].raise_()
            self.windows["tasks"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Assign Task")

        layout = QVBoxLayout()

        self.complaint_id = QLineEdit()
        self.emp_id = QLineEdit()
        self.title = QLineEdit()
        self.desc = QLineEdit()

        self.complaint_id.setPlaceholderText("Complaint ID")
        self.emp_id.setPlaceholderText("Employee ID")
        self.title.setPlaceholderText("Task Title")
        self.desc.setPlaceholderText("Description")

        btn = QPushButton("Assign Task")
        btn.clicked.connect(self.assign_task)

        layout.addWidget(self.complaint_id)
        layout.addWidget(self.emp_id)
        layout.addWidget(self.title)
        layout.addWidget(self.desc)
        layout.addWidget(btn)

        win.setLayout(layout)

        self.windows["tasks"] = win
        win.show()

    # ─────────────────────────────
    # ASSIGN TASK
    # ─────────────────────────────
    def assign_task(self):

        try:
            db.cursor.execute("""
                INSERT INTO tasks
                (
                    complaint_id,
                    dept_id,
                    assigned_to,
                    assigned_by,
                    title,
                    description,
                    priority,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(self.complaint_id.text()),
                1,
                int(self.emp_id.text()),
                self.user["data"]["emp_id"],
                self.title.text(),
                self.desc.text(),
                "High",
                "Pending"
            ))

            db.conn.commit()

            QMessageBox.information(
                self,
                "Success",
                "Task Assigned Successfully"
            )

        except Exception as e:
            print("❌ assign_task error:", e)

    # ─────────────────────────────
    # EMPLOYEES WINDOW
    # ─────────────────────────────
    def open_employees(self):

        if "employees" in self.windows:
            self.windows["employees"].raise_()
            self.windows["employees"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Employees")

        layout = QVBoxLayout()
        list_widget = QListWidget()

        try:
            db.cursor.execute("""
                SELECT emp_id, username, role
                FROM employees
            """)

            for row in db.cursor.fetchall():
                list_widget.addItem(f"{row[0]} - {row[1]} - {row[2]}")

        except Exception as e:
            print("❌ Employee load error:", e)

        layout.addWidget(list_widget)
        win.setLayout(layout)

        self.windows["employees"] = win
        win.show()

    # ─────────────────────────────
    # ANALYTICS WINDOW
    # ─────────────────────────────
    def open_analytics(self):

        if "analytics" in self.windows:
            self.windows["analytics"].raise_()
            self.windows["analytics"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Analytics Dashboard")

        layout = QVBoxLayout()

        try:
            db.cursor.execute("SELECT COUNT(*) FROM complaints")
            complaints = db.cursor.fetchone()[0]

            db.cursor.execute("SELECT COUNT(*) FROM tasks")
            tasks = db.cursor.fetchone()[0]

            db.cursor.execute("SELECT COUNT(*) FROM employees")
            employees = db.cursor.fetchone()[0]

            label = QLabel(
                f"📊 System Overview\n\n"
                f"Complaints: {complaints}\n"
                f"Tasks: {tasks}\n"
                f"Employees: {employees}"
            )

            label.setStyleSheet("font-size: 16px;")

            layout.addWidget(label)

        except Exception as e:
            print("❌ analytics error:", e)

        win.setLayout(layout)

        self.windows["analytics"] = win
        win.show()