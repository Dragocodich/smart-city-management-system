from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.database import db
from utils.logger import Logger


class EmployeePanel(QWidget):

    def __init__(self, user, on_logout=None):
        super().__init__()

        self.user = user
        self.logger = Logger()
        self.emp = user["data"]
        self.on_logout = on_logout

        self.setWindowTitle("Employee Dashboard")
        self.setGeometry(300, 200, 900, 600)

        # MAIN LAYOUT
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # ─────────────────────────────
        # HEADER
        # ─────────────────────────────
        header_layout = QHBoxLayout()
        
        title = QLabel(f"👷 {self.emp['full_name']} - Task Dashboard")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setMaximumWidth(120)
        logout_btn.setMinimumHeight(40)
        logout_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        logout_btn.setStyleSheet(self._get_logout_style())
        logout_btn.clicked.connect(self.logout)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)
        
        layout.addLayout(header_layout)

        # ─────────────────────────────
        # TASK LIST
        # ─────────────────────────────
        task_label = QLabel("📋 Assigned Tasks")
        task_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        task_label.setStyleSheet("color: #34495e;")
        
        self.task_list = QListWidget()
        self.task_list.setMinimumHeight(300)
        self.task_list.setStyleSheet(self._get_list_style())
        
        self.load_tasks()
        
        # ─────────────────────────────
        # TASK ACTIONS
        # ─────────────────────────────
        action_layout = QHBoxLayout()
        
        self.btn_complete = QPushButton("✅ Mark as Complete")
        self.btn_complete.setMinimumHeight(45)
        self.btn_complete.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_complete.setStyleSheet(self._get_button_style("#27ae60"))
        self.btn_complete.clicked.connect(self.complete_task)
        
        self.btn_view = QPushButton("👁️ View Details")
        self.btn_view.setMinimumHeight(45)
        self.btn_view.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_view.setStyleSheet(self._get_button_style("#3498db"))
        self.btn_view.clicked.connect(self.view_task_details)
        
        action_layout.addWidget(self.btn_complete)
        action_layout.addWidget(self.btn_view)
        
        # ─────────────────────────────
        # STATS
        # ─────────────────────────────
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.stats_pending = QLabel("📌 Pending: 0")
        self.stats_pending.setFont(QFont("Arial", 11))
        self.stats_pending.setStyleSheet("color: #e74c3c;")
        
        self.stats_completed = QLabel("✔️ Completed: 0")
        self.stats_completed.setFont(QFont("Arial", 11))
        self.stats_completed.setStyleSheet("color: #27ae60;")
        
        stats_layout.addWidget(self.stats_pending)
        stats_layout.addWidget(self.stats_completed)
        stats_layout.addStretch()
        
        # ─────────────────────────────
        # ADD ALL TO MAIN LAYOUT
        # ─────────────────────────────
        layout.addWidget(task_label)
        layout.addWidget(self.task_list)
        layout.addLayout(action_layout)
        layout.addLayout(stats_layout)
        layout.addStretch()

        self.setLayout(layout)

    def _get_list_style(self):
        """List widget styling"""
        return """
            QListWidget {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
                margin: 2px 0px;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
            }
        """

    def _get_button_style(self, color):
        """Button styling"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {self._darken_color(color)});
                color: white;
                border: none;
                border-radius: 8px;
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

    def _get_logout_style(self):
        """Logout button styling"""
        return """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """

    def _darken_color(self, color, factor=1):
        """Darken hex color"""
        color_map = {
            "#27ae60": ["#1e8449", "#186a3b", "#145a32"],
            "#3498db": ["#2980b9", "#1f618d", "#154360"],
        }
        return color_map.get(color, [color, color, color])[factor - 1] if factor > 0 else color

    # ─────────────────────────────
    # LOAD TASKS
    # ─────────────────────────────
    def load_tasks(self):
        """Load tasks assigned to employee"""
        self.task_list.clear()
        
        try:
            # In dev mode, show mock tasks
            mock_tasks = [
                {"id": 1, "title": "Fix street lights in Block A", "priority": "High", "status": "Pending"},
                {"id": 2, "title": "Repair traffic signal at Clifton", "priority": "High", "status": "In Progress"},
                {"id": 3, "title": "Collect waste from Zone 5", "priority": "Normal", "status": "Pending"},
            ]
            
            for task in mock_tasks:
                item_text = f"🔹 {task['title']}\n   Priority: {task['priority']} | Status: {task['status']}"
                self.task_list.addItem(item_text)
            
            self.logger.info(f"Loaded {len(mock_tasks)} tasks for {self.emp['full_name']}")
            self.stats_pending.setText(f"📌 Pending: {len([t for t in mock_tasks if t['status'] == 'Pending'])}")
            self.stats_completed.setText(f"✔️ Completed: 0")
            
        except Exception as e:
            self.logger.error(f"Error loading tasks: {e}")
            self.task_list.addItem("Error loading tasks")

    # ─────────────────────────────
    # COMPLETE TASK
    # ─────────────────────────────
    def complete_task(self):
        """Mark selected task as complete"""
        current = self.task_list.currentItem()
        
        if not current:
            QMessageBox.warning(self, "Error", "Please select a task")
            return
        
        try:
            self.logger.info(f"Task marked as complete by {self.emp['full_name']}")
            self.task_list.takeItem(self.task_list.row(current))
            QMessageBox.information(self, "Success", "✅ Task marked as complete!")
            self.load_tasks()
        except Exception as e:
            self.logger.error(f"Error completing task: {e}")
            QMessageBox.critical(self, "Error", f"Error updating task: {str(e)[:50]}")

    # ─────────────────────────────
    # VIEW TASK DETAILS
    # ─────────────────────────────
    def view_task_details(self):
        """View details of selected task"""
        current = self.task_list.currentItem()
        
        if not current:
            QMessageBox.warning(self, "Error", "Please select a task")
            return
        
        task_text = current.text()
        QMessageBox.information(self, "Task Details", f"📋 Details:\n{task_text}\n\nCreated: 2026-05-08\nDue: 2026-05-15")

    # ─────────────────────────────
    # LOGOUT
    # ─────────────────────────────
    def logout(self):
        """Logout and return to role selector"""
        self.logger.info(f"{self.emp['full_name']} logged out")
        
        # Call logout callback to close dashboard
        if self.on_logout:
            self.on_logout()
        else:
            # Fallback: close parent window
            parent = self.parent()
            if parent:
                parent.close()

    # ─────────────────────────────
    # COMPLETE TASK
    # ─────────────────────────────
    def complete_task(self):
        """Mark selected task as complete"""
        current = self.task_list.currentItem()
        
        if not current:
            QMessageBox.warning(self, "Error", "Please select a task")
            return
        
        try:
            self.logger.info(f"Task marked as complete by {self.emp['full_name']}")
            self.task_list.takeItem(self.task_list.row(current))
            QMessageBox.information(self, "Success", "✅ Task marked as complete!")
            self.load_tasks()
        except Exception as e:
            self.logger.error(f"Error completing task: {e}")
            QMessageBox.critical(self, "Error", f"Failed to complete task: {e}")