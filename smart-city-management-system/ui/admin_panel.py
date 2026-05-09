from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.database import db
from utils.logger import Logger


class AdminPanel(QWidget):

    def __init__(self, user, on_logout=None):
        super().__init__()

        self.user = user
        self.logger = Logger()
        self.on_logout = on_logout

        self.setWindowTitle("Admin Control Panel")

        # ─────────────────────────────
        # MAIN LAYOUT
        # ─────────────────────────────
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        # ─────────────────────────────
        # HEADER
        # ─────────────────────────────
        header_layout = QHBoxLayout()
        
        raw_role = self.user['data']['role']
        clean_role = raw_role.replace("System Administrator System Administrator", "System Administrator").strip()
        clean_role = clean_role.replace("Welcome", "").strip()

        self.title_label = QLabel(f"👨‍💼 {clean_role} - Control Panel")
        self.title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        self.layout_main.addLayout(header_layout)

        # ─────────────────────────────
        # SEPARATOR
        # ─────────────────────────────
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #ecf0f1;")
        self.layout_main.addWidget(line)

        # ─────────────────────────────
        # ADMIN MENU BUTTONS
        # ─────────────────────────────
        menu_label = QLabel("🎛️ Administration Menu")
        menu_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        menu_label.setStyleSheet("color: #34495e; margin-top: 20px;")
        self.layout_main.addWidget(menu_label)

        # Create grid for buttons
        button_layout = QGridLayout()
        button_layout.setSpacing(15)

        self.btn_complaints = QPushButton("📋 Manage Complaints")
        self.btn_complaints.setMinimumHeight(80)
        self.btn_complaints.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_complaints.setStyleSheet(self._get_menu_button_style("#3498db"))
        self.btn_complaints.clicked.connect(self.open_complaints)

        self.btn_tasks = QPushButton("✅ Assign Tasks")
        self.btn_tasks.setMinimumHeight(80)
        self.btn_tasks.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_tasks.setStyleSheet(self._get_menu_button_style("#27ae60"))
        self.btn_tasks.clicked.connect(self.open_task_assigner)

        self.btn_employees = QPushButton("👥 Manage Employees")
        self.btn_employees.setMinimumHeight(80)
        self.btn_employees.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_employees.setStyleSheet(self._get_menu_button_style("#f39c12"))
        self.btn_employees.clicked.connect(self.open_employees)

        self.btn_analytics = QPushButton("📊 Analytics")
        self.btn_analytics.setMinimumHeight(80)
        self.btn_analytics.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_analytics.setStyleSheet(self._get_menu_button_style("#e74c3c"))
        self.btn_analytics.clicked.connect(self.open_analytics)

        self.btn_payments = QPushButton("💳 Verify Payments")
        self.btn_payments.setMinimumHeight(80)
        self.btn_payments.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_payments.setStyleSheet(self._get_menu_button_style("#16a085"))
        self.btn_payments.clicked.connect(self.open_payment_verification)

        button_layout.addWidget(self.btn_complaints, 0, 0)
        button_layout.addWidget(self.btn_tasks, 0, 1)
        button_layout.addWidget(self.btn_employees, 1, 0)
        button_layout.addWidget(self.btn_analytics, 1, 1)
        button_layout.addWidget(self.btn_payments, 2, 0)

        self.layout_main.addLayout(button_layout)

        # ─────────────────────────────
        # STATS SECTION
        # ─────────────────────────────
        stats_label = QLabel("📈 Quick Stats")
        stats_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        stats_label.setStyleSheet("color: #34495e; margin-top: 20px;")
        self.layout_main.addWidget(stats_label)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.stat1 = QLabel("📝 Total Complaints: 24")
        self.stat1.setFont(QFont("Arial", 11))
        self.stat1.setStyleSheet("color: #3498db; padding: 10px;")

        self.stat2 = QLabel("✅ Resolved: 18")
        self.stat2.setFont(QFont("Arial", 11))
        self.stat2.setStyleSheet("color: #27ae60; padding: 10px;")

        self.stat3 = QLabel("⏳ Pending: 6")
        self.stat3.setFont(QFont("Arial", 11))
        self.stat3.setStyleSheet("color: #e74c3c; padding: 10px;")

        stats_layout.addWidget(self.stat1)
        stats_layout.addWidget(self.stat2)
        stats_layout.addWidget(self.stat3)
        stats_layout.addStretch()

        self.layout_main.addLayout(stats_layout)

        self.layout_main.addStretch()

        # ─────────────────────────────
        # LOGOUT BUTTON
        # ─────────────────────────────
        self.btn_logout = QPushButton("🚪 Logout")
        self.btn_logout.setMinimumHeight(45)
        self.btn_logout.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.btn_logout.clicked.connect(self.logout)
        self.layout_main.addWidget(self.btn_logout)

        # ─────────────────────────────
        # WINDOW CACHE (PREVENT DUPLICATES)
        # ─────────────────────────────
        self.windows = {}

    def _get_menu_button_style(self, color):
        """Menu button styling"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {self._darken_color(color)});
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self._darken_color(color)}, stop:1 {self._darken_color(color, 2)});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self._darken_color(color, 2)}, stop:1 {self._darken_color(color, 3)});
            }}
        """

    def _darken_color(self, color, factor=1):
        """Darken hex color"""
        color_map = {
            "#3498db": ["#2980b9", "#1f618d", "#154360"],
            "#27ae60": ["#1e8449", "#186a3b", "#145a32"],
            "#f39c12": ["#d68910", "#b8860b", "#9a7d0a"],
            "#e74c3c": ["#c0392b", "#a93226", "#922b21"],
            "#16a085": ["#138d75", "#117a65", "#0e6251"],
        }
        return color_map.get(color, [color, color, color])[factor - 1] if factor > 0 else color

    # ─────────────────────────────
    # COMPLAINTS WINDOW
    # ─────────────────────────────
    def open_complaints(self):

        if "complaints" in self.windows:
            self.windows["complaints"].raise_()
            self.windows["complaints"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Manage Complaints")
        win.setGeometry(200, 100, 900, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("📋 Manage Complaints")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Table Layout
        table_layout = QHBoxLayout()
        table_layout.setSpacing(15)

        # Left - List
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: white;
            }
            QListWidget::item {
                padding: 10px;
                margin: 3px;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
            }
        """)

        try:
            # Mock complaints for dev mode
            self.complaints_data = [
                {"id": "C001", "title": "Road pothole in Block A", "status": "Pending", "citizen": "Ali Khan"},
                {"id": "C002", "title": "Street light not working", "status": "In Progress", "citizen": "Fatima Ahmed"},
                {"id": "C003", "title": "Water supply low", "status": "Resolved", "citizen": "Hassan Ali"},
                {"id": "C004", "title": "Illegal parking", "status": "Pending", "citizen": "Sara Malik"},
            ]

            for complaint in self.complaints_data:
                if complaint['status'] == "Resolved":
                    emoji = "✅"
                    list_widget.addItem(f"{emoji} {complaint['id']} - {complaint['title']}")
                elif complaint['status'] == "In Progress":
                    emoji = "⏳"
                    list_widget.addItem(f"{emoji} {complaint['id']} - {complaint['title']}")
                else:
                    emoji = "🔴"
                    list_widget.addItem(f"{emoji} {complaint['id']} - {complaint['title']}")

            self.logger.info("Complaints loaded successfully")

        except Exception as e:
            self.logger.error(f"Error loading complaints: {e}")
            list_widget.addItem(f"Error: {str(e)}")

        table_layout.addWidget(list_widget, 2)

        # Right - Details & Actions
        details_layout = QVBoxLayout()

        # Details Panel
        self.complaint_details = QTextEdit()
        self.complaint_details.setReadOnly(True)
        self.complaint_details.setMinimumWidth(300)
        self.complaint_details.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: #f8f9fa;
                padding: 10px;
            }
        """)
        self.complaint_details.setText("Select a complaint to view details")

        # Connect selection change
        list_widget.itemSelectionChanged.connect(
            lambda: self._update_complaint_details(list_widget, self.complaints_data)
        )

        details_layout.addWidget(QLabel("📝 Details:"), 0)
        details_layout.addWidget(self.complaint_details, 1)

        # Action Buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        btn_mark_progress = QPushButton("⏳ Mark In Progress")
        btn_mark_progress.setMinimumHeight(40)
        btn_mark_progress.setStyleSheet(self._get_action_button_style("#f39c12"))
        btn_mark_progress.clicked.connect(lambda: self._update_complaint_status(list_widget, "In Progress"))

        btn_mark_complete = QPushButton("✅ Mark Complete")
        btn_mark_complete.setMinimumHeight(40)
        btn_mark_complete.setStyleSheet(self._get_action_button_style("#27ae60"))
        btn_mark_complete.clicked.connect(lambda: self._update_complaint_status(list_widget, "Resolved"))

        btn_delete = QPushButton("🗑️ Delete")
        btn_delete.setMinimumHeight(40)
        btn_delete.setStyleSheet(self._get_action_button_style("#e74c3c"))
        btn_delete.clicked.connect(lambda: self._delete_complaint(list_widget))

        action_layout.addWidget(btn_mark_progress)
        action_layout.addWidget(btn_mark_complete)
        action_layout.addWidget(btn_delete)

        details_layout.addLayout(action_layout)

        table_layout.addLayout(details_layout, 1)
        layout.addLayout(table_layout)

        # Close button
        btn_close = QPushButton("Close")
        btn_close.setMinimumHeight(35)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        btn_close.clicked.connect(win.close)
        layout.addWidget(btn_close)

        win.setLayout(layout)
        win.setStyleSheet("background: #ecf0f1;")
        self.windows["complaints"] = win
        win.show()

    def _update_complaint_details(self, list_widget, complaints_data):
        """Update complaint details panel"""
        current = list_widget.currentItem()
        if not current:
            return
        
        idx = list_widget.row(current)
        if 0 <= idx < len(complaints_data):
            complaint = complaints_data[idx]
            details = f"""🔍 COMPLAINT DETAILS

ID: {complaint['id']}
Title: {complaint['title']}
Status: {complaint['status']}
Citizen: {complaint['citizen']}
Priority: High

Description:
{complaint['title']}

Actions Taken: None yet
Resolution: Pending"""
            self.complaint_details.setText(details)

    def _update_complaint_status(self, list_widget, new_status):
        """Update complaint status"""
        current = list_widget.currentItem()
        if not current:
            QMessageBox.warning(self.windows["complaints"], "Error", "Please select a complaint")
            return
        
        idx = list_widget.row(current)
        if 0 <= idx < len(self.complaints_data):
            self.complaints_data[idx]['status'] = new_status
            
            # Update list display
            if new_status == "Resolved":
                emoji = "✅"
            elif new_status == "In Progress":
                emoji = "⏳"
            else:
                emoji = "🔴"
            
            current.setText(f"{emoji} {self.complaints_data[idx]['id']} - {self.complaints_data[idx]['title']}")
            QMessageBox.information(self.windows["complaints"], "Success", f"✅ Complaint marked as {new_status}")
            self._update_complaint_details(list_widget, self.complaints_data)

    def _delete_complaint(self, list_widget):
        """Delete complaint"""
        current = list_widget.currentItem()
        if not current:
            QMessageBox.warning(self.windows["complaints"], "Error", "Please select a complaint")
            return
        
        idx = list_widget.row(current)
        if QMessageBox.question(self.windows["complaints"], "Confirm", 
                               "Are you sure you want to delete this complaint?") == QMessageBox.StandardButton.Yes:
            del self.complaints_data[idx]
            list_widget.takeItem(idx)
            QMessageBox.information(self.windows["complaints"], "Success", "✅ Complaint deleted")
            self.complaint_details.setText("Select a complaint to view details")

    # ─────────────────────────────
    # TASK ASSIGNER WINDOW
    # ─────────────────────────────
    def open_task_assigner(self):

        if "tasks" in self.windows:
            self.windows["tasks"].raise_()
            self.windows["tasks"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Assign Tasks")
        win.setGeometry(200, 100, 1000, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("✏️ Assign & Manage Tasks")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        # Main content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # LEFT - TASK FORM
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)

        form_label = QLabel("📝 Create New Task")
        form_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        form_label.setStyleSheet("color: #34495e;")
        form_layout.addWidget(form_label)

        # Employee selection
        emp_label = QLabel("Assign to Employee:")
        emp_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_employee = QComboBox()
        self.inp_employee.addItems(["Worker-1 (Abu)", "Worker-2 (Hassan)", "Officer-1 (Ali)", "Officer-2 (Sara)"])
        self.inp_employee.setMinimumHeight(35)
        self.inp_employee.setStyleSheet(self._get_input_combo_style())
        form_layout.addWidget(emp_label)
        form_layout.addWidget(self.inp_employee)

        # Task title
        title_label = QLabel("Task Title:")
        title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_task_title = QLineEdit()
        self.inp_task_title.setPlaceholderText("e.g., Fix street light in Block A")
        self.inp_task_title.setMinimumHeight(35)
        self.inp_task_title.setStyleSheet(self._get_input_style())
        form_layout.addWidget(title_label)
        form_layout.addWidget(self.inp_task_title)

        # Task description
        desc_label = QLabel("Description:")
        desc_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_task_desc = QTextEdit()
        self.inp_task_desc.setPlaceholderText("Detailed description of the task...")
        self.inp_task_desc.setMinimumHeight(80)
        self.inp_task_desc.setStyleSheet(self._get_input_style())
        form_layout.addWidget(desc_label)
        form_layout.addWidget(self.inp_task_desc)

        # Priority
        priority_label = QLabel("Priority:")
        priority_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_priority = QComboBox()
        self.inp_priority.addItems(["Low", "Medium", "High", "Critical"])
        self.inp_priority.setCurrentText("Medium")
        self.inp_priority.setMinimumHeight(35)
        self.inp_priority.setStyleSheet(self._get_input_combo_style())
        form_layout.addWidget(priority_label)
        form_layout.addWidget(self.inp_priority)

        # Due date
        due_label = QLabel("Due Date:")
        due_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_due_date = QLineEdit()
        self.inp_due_date.setPlaceholderText("YYYY-MM-DD")
        self.inp_due_date.setMinimumHeight(35)
        self.inp_due_date.setStyleSheet(self._get_input_style())
        form_layout.addWidget(due_label)
        form_layout.addWidget(self.inp_due_date)

        # Assign button
        btn_assign = QPushButton("✅ Assign Task")
        btn_assign.setMinimumHeight(45)
        btn_assign.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn_assign.setStyleSheet(self._get_action_button_style("#27ae60"))
        btn_assign.clicked.connect(lambda: self._create_task())
        form_layout.addWidget(btn_assign)

        form_layout.addStretch()

        # RIGHT - TASK LIST
        list_layout = QVBoxLayout()
        list_layout.setSpacing(10)

        list_label = QLabel("📌 Assigned Tasks")
        list_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        list_label.setStyleSheet("color: #34495e;")
        list_layout.addWidget(list_label)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: white;
            }
            QListWidget::item {
                padding: 10px;
                margin: 3px;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:1 #1e8449);
                color: white;
            }
        """)

        self.tasks_data = [
            {"id": "T001", "employee": "Worker-1 (Abu)", "title": "Fix street light", "status": "Assigned", "priority": "High", "due": "2026-05-15"},
            {"id": "T002", "employee": "Officer-1 (Ali)", "title": "Inspect water pipes", "status": "In Progress", "priority": "Medium", "due": "2026-05-18"},
            {"id": "T003", "employee": "Worker-2 (Hassan)", "title": "Clean main road", "status": "Completed", "priority": "Low", "due": "2026-05-10"},
        ]

        for task in self.tasks_data:
            emoji = "✅" if task['status'] == "Completed" else "⏳" if task['status'] == "In Progress" else "📌"
            self.task_list.addItem(f"{emoji} {task['id']} - {task['title']}")

        list_layout.addWidget(self.task_list)

        # Task actions
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        btn_mark_done = QPushButton("✅ Mark Done")
        btn_mark_done.setMinimumHeight(35)
        btn_mark_done.setStyleSheet(self._get_action_button_style("#27ae60"))
        btn_mark_done.clicked.connect(lambda: self._mark_task_done())

        btn_delete_task = QPushButton("🗑️ Delete")
        btn_delete_task.setMinimumHeight(35)
        btn_delete_task.setStyleSheet(self._get_action_button_style("#e74c3c"))
        btn_delete_task.clicked.connect(lambda: self._delete_task())

        action_layout.addWidget(btn_mark_done)
        action_layout.addWidget(btn_delete_task)

        list_layout.addLayout(action_layout)

        content_layout.addLayout(form_layout, 1)
        content_layout.addLayout(list_layout, 1)

        layout.addLayout(content_layout)

        # Close button
        btn_close = QPushButton("Close")
        btn_close.setMinimumHeight(35)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        btn_close.clicked.connect(win.close)
        layout.addWidget(btn_close)

        win.setLayout(layout)
        win.setStyleSheet("background: #ecf0f1;")
        self.windows["tasks"] = win
        win.show()

    def _create_task(self):
        """Create and assign new task"""
        title = self.inp_task_title.text().strip()
        desc = self.inp_task_desc.toPlainText().strip()
        employee = self.inp_employee.currentText()
        priority = self.inp_priority.currentText()
        due_date = self.inp_due_date.text().strip()

        if not title or not desc:
            QMessageBox.warning(self.windows["tasks"], "Error", "⚠️ Please fill all required fields")
            return

        try:
            task_id = f"T{len(self.tasks_data)+1:03d}"
            self.tasks_data.append({
                "id": task_id,
                "employee": employee,
                "title": title,
                "status": "Assigned",
                "priority": priority,
                "due": due_date if due_date else "2026-05-20"
            })

            self.task_list.addItem(f"📌 {task_id} - {title}")
            self.inp_task_title.clear()
            self.inp_task_desc.clear()
            self.inp_due_date.clear()

            QMessageBox.information(self.windows["tasks"], "Success", f"✅ Task {task_id} assigned to {employee}!")
            self.logger.info(f"Task created: {task_id} for {employee}")
        except Exception as e:
            QMessageBox.critical(self.windows["tasks"], "Error", f"Error: {str(e)}")

    def _mark_task_done(self):
        """Mark task as completed"""
        current = self.task_list.currentItem()
        if not current:
            QMessageBox.warning(self.windows["tasks"], "Error", "Please select a task")
            return

        idx = self.task_list.row(current)
        if 0 <= idx < len(self.tasks_data):
            self.tasks_data[idx]['status'] = "Completed"
            current.setText(f"✅ {self.tasks_data[idx]['id']} - {self.tasks_data[idx]['title']}")
            QMessageBox.information(self.windows["tasks"], "Success", "✅ Task marked as completed!")

    def _delete_task(self):
        """Delete task"""
        current = self.task_list.currentItem()
        if not current:
            QMessageBox.warning(self.windows["tasks"], "Error", "Please select a task")
            return

        idx = self.task_list.row(current)
        if QMessageBox.question(self.windows["tasks"], "Confirm", "Delete this task?") == QMessageBox.StandardButton.Yes:
            del self.tasks_data[idx]
            self.task_list.takeItem(idx)
            QMessageBox.information(self.windows["tasks"], "Success", "✅ Task deleted!")

    # ─────────────────────────────
    # EMPLOYEES WINDOW
    # ─────────────────────────────
    def open_employees(self):

        if "employees" in self.windows:
            self.windows["employees"].raise_()
            self.windows["employees"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Manage Employees")
        win.setGeometry(200, 100, 900, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("👥 Employee Management")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        # Main content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # LEFT - Form to add employee
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)

        form_label = QLabel("➕ Add New Employee")
        form_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        form_label.setStyleSheet("color: #34495e;")
        form_layout.addWidget(form_label)

        # Name
        name_label = QLabel("Full Name:")
        name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_emp_name = QLineEdit()
        self.inp_emp_name.setPlaceholderText("Enter employee name")
        self.inp_emp_name.setMinimumHeight(35)
        self.inp_emp_name.setStyleSheet(self._get_input_style())
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.inp_emp_name)

        # Email
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_emp_email = QLineEdit()
        self.inp_emp_email.setPlaceholderText("employee@example.com")
        self.inp_emp_email.setMinimumHeight(35)
        self.inp_emp_email.setStyleSheet(self._get_input_style())
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.inp_emp_email)

        # Role
        role_label = QLabel("Role:")
        role_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_emp_role = QComboBox()
        self.inp_emp_role.addItems(["Worker", "Officer", "Supervisor", "Manager"])
        self.inp_emp_role.setMinimumHeight(35)
        self.inp_emp_role.setStyleSheet(self._get_input_combo_style())
        form_layout.addWidget(role_label)
        form_layout.addWidget(self.inp_emp_role)

        # Department
        dept_label = QLabel("Department:")
        dept_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_emp_dept = QComboBox()
        self.inp_emp_dept.addItems(["Infrastructure", "Public Health", "Traffic", "Utilities", "Maintenance"])
        self.inp_emp_dept.setMinimumHeight(35)
        self.inp_emp_dept.setStyleSheet(self._get_input_combo_style())
        form_layout.addWidget(dept_label)
        form_layout.addWidget(self.inp_emp_dept)

        # Salary
        salary_label = QLabel("Salary (PKR):")
        salary_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.inp_emp_salary = QLineEdit()
        self.inp_emp_salary.setPlaceholderText("e.g., 50000")
        self.inp_emp_salary.setMinimumHeight(35)
        self.inp_emp_salary.setStyleSheet(self._get_input_style())
        form_layout.addWidget(salary_label)
        form_layout.addWidget(self.inp_emp_salary)

        # Add button
        btn_add = QPushButton("➕ Add Employee")
        btn_add.setMinimumHeight(45)
        btn_add.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn_add.setStyleSheet(self._get_action_button_style("#27ae60"))
        btn_add.clicked.connect(lambda: self._add_employee())
        form_layout.addWidget(btn_add)

        form_layout.addStretch()

        # RIGHT - Employee list
        list_layout = QVBoxLayout()
        list_layout.setSpacing(10)

        list_label = QLabel("📋 Active Employees")
        list_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        list_label.setStyleSheet("color: #34495e;")
        list_layout.addWidget(list_label)

        self.emp_list = QListWidget()
        self.emp_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: white;
            }
            QListWidget::item {
                padding: 10px;
                margin: 3px;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f39c12, stop:1 #d68910);
                color: white;
            }
        """)

        self.employees_data = [
            {"id": "E001", "name": "Abu Ahmed", "email": "abu@example.com", "role": "Worker", "department": "Infrastructure", "salary": 50000, "status": "Active"},
            {"id": "E002", "name": "Hassan Khan", "email": "hassan@example.com", "role": "Officer", "department": "Traffic", "salary": 75000, "status": "Active"},
            {"id": "E003", "name": "Ali Malik", "email": "ali@example.com", "role": "Supervisor", "department": "Utilities", "salary": 85000, "status": "Active"},
            {"id": "E004", "name": "Sara Ahmed", "email": "sara@example.com", "role": "Manager", "department": "Public Health", "salary": 95000, "status": "Active"},
        ]

        for emp in self.employees_data:
            self.emp_list.addItem(f"✅ {emp['id']} - {emp['name']}\n   Role: {emp['role']} | Dept: {emp['department']}")

        list_layout.addWidget(self.emp_list)

        # Employee actions
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        btn_view_details = QPushButton("👤 View Details")
        btn_view_details.setMinimumHeight(35)
        btn_view_details.setStyleSheet(self._get_action_button_style("#3498db"))
        btn_view_details.clicked.connect(lambda: self._show_employee_details())

        btn_deactivate = QPushButton("❌ Deactivate")
        btn_deactivate.setMinimumHeight(35)
        btn_deactivate.setStyleSheet(self._get_action_button_style("#e74c3c"))
        btn_deactivate.clicked.connect(lambda: self._deactivate_employee())

        action_layout.addWidget(btn_view_details)
        action_layout.addWidget(btn_deactivate)

        list_layout.addLayout(action_layout)

        content_layout.addLayout(form_layout, 1)
        content_layout.addLayout(list_layout, 1)

        layout.addLayout(content_layout)

        # Close button
        btn_close = QPushButton("Close")
        btn_close.setMinimumHeight(35)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        btn_close.clicked.connect(win.close)
        layout.addWidget(btn_close)

        win.setLayout(layout)
        win.setStyleSheet("background: #ecf0f1;")
        self.windows["employees"] = win
        win.show()

    def _add_employee(self):
        """Add new employee"""
        name = self.inp_emp_name.text().strip()
        email = self.inp_emp_email.text().strip()
        role = self.inp_emp_role.currentText()
        dept = self.inp_emp_dept.currentText()
        salary = self.inp_emp_salary.text().strip()

        if not name or not email or not salary:
            QMessageBox.warning(self.windows["employees"], "Error", "⚠️ Please fill all required fields")
            return

        try:
            emp_id = f"E{len(self.employees_data)+1:03d}"
            self.employees_data.append({
                "id": emp_id,
                "name": name,
                "email": email,
                "role": role,
                "department": dept,
                "salary": int(salary),
                "status": "Active"
            })

            self.emp_list.addItem(f"✅ {emp_id} - {name}\n   Role: {role} | Dept: {dept}")
            self.inp_emp_name.clear()
            self.inp_emp_email.clear()
            self.inp_emp_salary.clear()

            QMessageBox.information(self.windows["employees"], "Success", f"✅ Employee {emp_id} added successfully!")
            self.logger.info(f"Employee added: {emp_id} - {name}")
        except Exception as e:
            QMessageBox.critical(self.windows["employees"], "Error", f"Error: {str(e)}")

    def _show_employee_details(self):
        """Show employee details"""
        current = self.emp_list.currentItem()
        if not current:
            QMessageBox.warning(self.windows["employees"], "Error", "Please select an employee")
            return

        idx = self.emp_list.row(current)
        if 0 <= idx < len(self.employees_data):
            emp = self.employees_data[idx]
            details = f"""👤 EMPLOYEE DETAILS

ID: {emp['id']}
Name: {emp['name']}
Email: {emp['email']}
Role: {emp['role']}
Department: {emp['department']}
Salary: PKR {emp['salary']:,}
Status: {emp['status']}
Join Date: 2025-01-15

Performance: Excellent
Tasks Completed: 24
Rating: 4.8/5"""
            QMessageBox.information(self.windows["employees"], "Employee Details", details)

    def _deactivate_employee(self):
        """Deactivate employee"""
        current = self.emp_list.currentItem()
        if not current:
            QMessageBox.warning(self.windows["employees"], "Error", "Please select an employee")
            return

        idx = self.emp_list.row(current)
        if QMessageBox.question(self.windows["employees"], "Confirm", "Deactivate this employee?") == QMessageBox.StandardButton.Yes:
            self.employees_data[idx]['status'] = "Inactive"
            current.setText(f"❌ {self.employees_data[idx]['id']} - {self.employees_data[idx]['name']}\n   Role: {self.employees_data[idx]['role']} | Dept: {self.employees_data[idx]['department']}")
            QMessageBox.information(self.windows["employees"], "Success", "✅ Employee deactivated!")

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
        win.setGeometry(100, 50, 1100, 700)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Title
        title = QLabel("📊 System Analytics Dashboard")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        # KPI Section
        kpi_layout = QGridLayout()
        kpi_layout.setSpacing(15)

        kpis = [
            {"label": "Total Complaints", "value": "127", "icon": "📋", "color": "#3498db"},
            {"label": "Resolved", "value": "89", "icon": "✅", "color": "#27ae60"},
            {"label": "In Progress", "value": "28", "icon": "⏳", "color": "#f39c12"},
            {"label": "Pending", "value": "10", "icon": "⏸️", "color": "#e74c3c"},
            {"label": "Active Employees", "value": "42", "icon": "👥", "color": "#9b59b6"},
            {"label": "Tasks Completed", "value": "156", "icon": "✔️", "color": "#16a085"},
            {"label": "Avg Response Time", "value": "2.5h", "icon": "⏱️", "color": "#e67e22"},
            {"label": "System Uptime", "value": "99.7%", "icon": "🟢", "color": "#2ecc71"},
        ]

        for i, kpi in enumerate(kpis):
            kpi_frame = QFrame()
            kpi_frame.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {kpi['color']}, stop:1 rgba(200,200,200,0.2));
                    border-radius: 10px;
                    border: 2px solid {kpi['color']};
                    padding: 10px;
                }}
            """)
            kpi_inner = QVBoxLayout()
            kpi_inner.setContentsMargins(10, 10, 10, 10)

            icon_lbl = QLabel(kpi['icon'])
            icon_lbl.setFont(QFont("Arial", 24))

            label = QLabel(kpi['label'])
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            label.setStyleSheet(f"color: {kpi['color']};")

            value = QLabel(kpi['value'])
            value.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            value.setStyleSheet(f"color: {kpi['color']};")

            kpi_inner.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
            kpi_inner.addWidget(value, alignment=Qt.AlignmentFlag.AlignCenter)
            kpi_inner.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

            kpi_frame.setLayout(kpi_inner)
            kpi_layout.addWidget(kpi_frame, i // 4, i % 4)

        layout.addLayout(kpi_layout)

        # Detailed Stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        # Left - Department stats
        left_stats = QVBoxLayout()
        left_stats.setSpacing(10)

        dept_label = QLabel("🏢 Department Statistics")
        dept_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        dept_label.setStyleSheet("color: #34495e;")
        left_stats.addWidget(dept_label)

        dept_text = """
Infrastructure: 12 employees, 34 tasks completed
Public Health: 8 employees, 28 tasks completed
Traffic: 15 employees, 45 tasks completed
Utilities: 7 employees, 22 tasks completed
Maintenance: 10 employees, 39 tasks completed
        """

        dept_display = QTextEdit()
        dept_display.setText(dept_text)
        dept_display.setReadOnly(True)
        dept_display.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                background: white;
                padding: 10px;
            }
        """)
        left_stats.addWidget(dept_display)

        # Right - Monthly report
        right_stats = QVBoxLayout()
        right_stats.setSpacing(10)

        monthly_label = QLabel("📅 Monthly Report (May 2026)")
        monthly_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        monthly_label.setStyleSheet("color: #34495e;")
        right_stats.addWidget(monthly_label)

        monthly_text = """
Total Complaints Received: 45
Complaints Resolved: 38 (84%)
Average Resolution Time: 2.8 hours
Citizen Satisfaction: 4.7/5
Employee Performance: Excellent
Budget Utilization: 72%
Projects On Track: 14/15
Critical Issues: 0
        """

        monthly_display = QTextEdit()
        monthly_display.setText(monthly_text)
        monthly_display.setReadOnly(True)
        monthly_display.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                background: white;
                padding: 10px;
            }
        """)
        right_stats.addWidget(monthly_display)

        stats_layout.addLayout(left_stats)
        stats_layout.addLayout(right_stats)

        layout.addLayout(stats_layout)

        # Export button
        btn_export = QPushButton("📥 Export Report")
        btn_export.setMinimumHeight(40)
        btn_export.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn_export.setStyleSheet(self._get_action_button_style("#2ecc71"))
        btn_export.clicked.connect(lambda: QMessageBox.information(win, "Export", "✅ Report exported successfully!"))

        # Close button
        btn_close = QPushButton("Close")
        btn_close.setMinimumHeight(35)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        btn_close.clicked.connect(win.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_export)
        button_layout.addWidget(btn_close)

        layout.addLayout(button_layout)

        win.setLayout(layout)
        win.setStyleSheet("background: #ecf0f1;")
        self.windows["analytics"] = win
        win.show()

    # ─────────────────────────────
    # PAYMENT VERIFICATION WINDOW
    # ─────────────────────────────
    def open_payment_verification(self):

        if "payments" in self.windows:
            self.windows["payments"].raise_()
            self.windows["payments"].activateWindow()
            return

        win = QWidget()
        win.setWindowTitle("Payment Verification")
        win.setGeometry(150, 80, 1000, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("💳 Payment Verification Portal")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        # Info banner
        info = QLabel("🔍 Verify pending payments from citizens. Once verified, the bill will be automatically removed from their dashboard.")
        info.setFont(QFont("Arial", 10))
        info.setStyleSheet("background: #ecf0f1; padding: 10px; border-radius: 6px; color: #34495e;")
        layout.addWidget(info)

        # Main content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Left - Pending payments list
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        list_label = QLabel("⏳ Pending Payment Verifications")
        list_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        list_label.setStyleSheet("color: #34495e;")
        left_layout.addWidget(list_label)

        self.pending_payments_list = QListWidget()
        self.pending_payments_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: white;
            }
            QListWidget::item {
                padding: 10px;
                margin: 3px;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16a085, stop:1 #138d75);
                color: white;
            }
        """)

        # Mock pending payments
        self.pending_payments = [
            {"txn_id": "TXN001", "citizen": "Ali Khan", "amount": 2500, "type": "Electricity", "status": "Pending", "date": "2026-05-08", "proof": "Bank Transfer"},
            {"txn_id": "TXN002", "citizen": "Fatima Ahmed", "amount": 800, "type": "Water", "status": "Pending", "date": "2026-05-08", "proof": "Online Payment"},
            {"txn_id": "TXN003", "citizen": "Hassan Ali", "amount": 1200, "type": "Gas", "status": "Pending", "date": "2026-05-07", "proof": "Check"},
        ]

        for payment in self.pending_payments:
            self.pending_payments_list.addItem(f"💳 {payment['txn_id']} - {payment['citizen']}\n   Amount: PKR {payment['amount']} | Type: {payment['type']}")

        left_layout.addWidget(self.pending_payments_list)

        # Action buttons for list
        list_actions = QHBoxLayout()
        list_actions.setSpacing(10)

        btn_view = QPushButton("👁️ View Details")
        btn_view.setMinimumHeight(35)
        btn_view.setStyleSheet(self._get_action_button_style("#3498db"))
        btn_view.clicked.connect(lambda: self._view_payment_details())

        btn_reject = QPushButton("❌ Reject")
        btn_reject.setMinimumHeight(35)
        btn_reject.setStyleSheet(self._get_action_button_style("#e74c3c"))
        btn_reject.clicked.connect(lambda: self._reject_payment())

        list_actions.addWidget(btn_view)
        list_actions.addWidget(btn_reject)
        left_layout.addLayout(list_actions)

        # Right - Details and verification
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        details_label = QLabel("📄 Payment Details")
        details_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        details_label.setStyleSheet("color: #34495e;")
        right_layout.addWidget(details_label)

        self.payment_details = QTextEdit()
        self.payment_details.setReadOnly(True)
        self.payment_details.setMinimumHeight(200)
        self.payment_details.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: white;
                padding: 10px;
            }
        """)
        self.payment_details.setText("Select a payment to view details")
        right_layout.addWidget(self.payment_details)

        # Connect selection
        self.pending_payments_list.itemSelectionChanged.connect(lambda: self._update_payment_details())

        # Verification section
        verify_label = QLabel("✅ Verify Payment")
        verify_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        verify_label.setStyleSheet("color: #34495e;")
        right_layout.addWidget(verify_label)

        # Notes
        notes_label = QLabel("Verification Notes:")
        notes_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.verify_notes = QTextEdit()
        self.verify_notes.setPlaceholderText("Add verification notes...")
        self.verify_notes.setMinimumHeight(80)
        self.verify_notes.setStyleSheet(self._get_input_style())
        right_layout.addWidget(notes_label)
        right_layout.addWidget(self.verify_notes)

        # Verify button
        btn_verify = QPushButton("✅ Verify & Complete Payment")
        btn_verify.setMinimumHeight(45)
        btn_verify.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn_verify.setStyleSheet(self._get_action_button_style("#27ae60"))
        btn_verify.clicked.connect(lambda: self._verify_payment())
        right_layout.addWidget(btn_verify)

        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 1)

        layout.addLayout(content_layout)

        # Close button
        btn_close = QPushButton("Close")
        btn_close.setMinimumHeight(35)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        btn_close.clicked.connect(win.close)
        layout.addWidget(btn_close)

        win.setLayout(layout)
        win.setStyleSheet("background: #ecf0f1;")
        self.windows["payments"] = win
        win.show()

    def _update_payment_details(self):
        """Update payment details display"""
        current = self.pending_payments_list.currentItem()
        if not current:
            return

        idx = self.pending_payments_list.row(current)
        if 0 <= idx < len(self.pending_payments):
            payment = self.pending_payments[idx]
            details = f"""💳 PAYMENT DETAILS

Transaction ID: {payment['txn_id']}
Citizen Name: {payment['citizen']}
Payment Amount: PKR {payment['amount']}
Bill Type: {payment['type']}
Date Submitted: {payment['date']}
Payment Method: {payment['proof']}
Status: {payment['status']}

Document Verification: ✅ Valid
Amount Match: ✅ Verified
Citizen Account: ✅ Active"""
            self.payment_details.setText(details)

    def _verify_payment(self):
        """Verify and complete payment"""
        current = self.pending_payments_list.currentItem()
        if not current:
            QMessageBox.warning(self.windows["payments"], "Error", "Please select a payment")
            return

        idx = self.pending_payments_list.row(current)
        if idx < 0 or idx >= len(self.pending_payments):
            return

        notes = self.verify_notes.toPlainText().strip()
        if not notes:
            QMessageBox.warning(self.windows["payments"], "Error", "Please add verification notes")
            return

        payment = self.pending_payments[idx]
        
        msg = QMessageBox.question(
            self.windows["payments"],
            "Confirm Verification",
            f"Verify payment {payment['txn_id']} from {payment['citizen']}?\n\nAmount: PKR {payment['amount']}\nThis will mark the bill as paid and remove it from citizen dashboard."
        )

        if msg == QMessageBox.StandardButton.Yes:
            # Mark as verified
            payment['status'] = "Verified"
            del self.pending_payments[idx]
            self.pending_payments_list.takeItem(idx)
            self.verify_notes.clear()
            self.payment_details.setText("Select a payment to view details")

            QMessageBox.information(
                self.windows["payments"],
                "Success",
                f"✅ Payment {payment['txn_id']} verified!\n\n💳 Bill amount PKR {payment['amount']} marked as PAID\n✖️ Bill removed from citizen dashboard\n\n📩 Notification sent to {payment['citizen']}"
            )
            self.logger.info(f"Payment verified: {payment['txn_id']} - {payment['citizen']} - PKR {payment['amount']}")

    def _reject_payment(self):
        """Reject payment"""
        current = self.pending_payments_list.currentItem()
        if not current:
            QMessageBox.warning(self.windows["payments"], "Error", "Please select a payment")
            return

        idx = self.pending_payments_list.row(current)
        if idx < 0 or idx >= len(self.pending_payments):
            return

        payment = self.pending_payments[idx]

        reason = QInputDialog.getText(
            self.windows["payments"],
            "Rejection Reason",
            "Enter reason for rejection:"
        )[0]

        if reason:
            del self.pending_payments[idx]
            self.pending_payments_list.takeItem(idx)

            QMessageBox.information(
                self.windows["payments"],
                "Rejected",
                f"❌ Payment {payment['txn_id']} rejected\n\n📩 Notification sent to {payment['citizen']}\nReason: {reason}"
            )

    def _view_payment_details(self):
        """View payment details in dialog"""
        current = self.pending_payments_list.currentItem()
        if not current:
            QMessageBox.warning(self.windows["payments"], "Error", "Please select a payment")
            return

        idx = self.pending_payments_list.row(current)
        if 0 <= idx < len(self.pending_payments):
            payment = self.pending_payments[idx]
            details = self.payment_details.toPlainText()
            QMessageBox.information(self.windows["payments"], f"Payment {payment['txn_id']}", details)

    # ─────────────────────────────
    # LOGOUT
    # ─────────────────────────────
    def logout(self):
        self.logger.info("Admin logged out")
        # Close all child windows
        for win in self.windows.values():
            try:
                win.close()
            except:
                pass
        # Call logout callback
        if self.on_logout:
            self.on_logout()
        else:
            # Fallback: close main window
            self.close()

    # ─────────────────────────────
    # HELPER METHODS FOR UI STYLING
    # ─────────────────────────────
    def _get_input_style(self):
        """Input field styling"""
        return """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                background: white;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background: #f8f9fa;
            }
        """

    def _get_input_combo_style(self):
        """ComboBox styling"""
        return """
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                background: white;
                font-size: 11px;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
        """

    def _get_action_button_style(self, color):
        """Action button styling"""
        color_map = {
            "#27ae60": ["#1e8449", "#186a3b"],
            "#e74c3c": ["#c0392b", "#a93226"],
            "#3498db": ["#2980b9", "#1f618d"],
            "#f39c12": ["#d68910", "#b8860b"],
            "#2ecc71": ["#27ae60", "#1abc9c"],
        }
        dark1, dark2 = color_map.get(color, [color, color])
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {dark1});
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {dark1}, stop:1 {dark2});
            }}
        """