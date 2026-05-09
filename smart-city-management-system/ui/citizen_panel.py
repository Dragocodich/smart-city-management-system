from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.database import db
from utils.logger import Logger


class CitizenPanel(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user["data"]
        self.logger = Logger()

        self.setWindowTitle("Citizen Dashboard")
        self.setGeometry(300, 200, 950, 650)

        # MAIN LAYOUT
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # ─────────────────────────────
        # HEADER
        # ─────────────────────────────
        header_layout = QHBoxLayout()
        
        title = QLabel(f"👤 {self.user['full_name']} - Citizen Portal")
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
        # TWO-COLUMN LAYOUT
        # ─────────────────────────────
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # LEFT COLUMN - COMPLAINTS
        left_layout = QVBoxLayout()
        
        complaint_label = QLabel("📝 Submit Complaint")
        complaint_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        complaint_label.setStyleSheet("color: #34495e;")
        
        self.complaint_input = QTextEdit()
        self.complaint_input.setPlaceholderText("Describe your complaint here...")
        self.complaint_input.setMinimumHeight(120)
        self.complaint_input.setStyleSheet(self._get_input_style())
        
        submit_btn = QPushButton("✉️ Submit Complaint")
        submit_btn.setMinimumHeight(45)
        submit_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        submit_btn.setStyleSheet(self._get_button_style("#e74c3c"))
        submit_btn.clicked.connect(self.submit_complaint)
        
        # RECENT COMPLAINTS
        recent_label = QLabel("🔔 Recent Complaints")
        recent_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        recent_label.setStyleSheet("color: #34495e;")
        
        self.recent_list = QListWidget()
        self.recent_list.setMinimumHeight(150)
        self.recent_list.setStyleSheet(self._get_list_style())
        self.load_recent_complaints()
        
        left_layout.addWidget(complaint_label)
        left_layout.addWidget(self.complaint_input)
        left_layout.addWidget(submit_btn)
        left_layout.addWidget(recent_label)
        left_layout.addWidget(self.recent_list)

        # RIGHT COLUMN - BILLS
        right_layout = QVBoxLayout()
        
        bills_label = QLabel("💳 Your Bills & Payments")
        bills_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        bills_label.setStyleSheet("color: #34495e;")
        
        self.payment_list = QListWidget()
        self.payment_list.setMinimumHeight(300)
        self.payment_list.setStyleSheet(self._get_list_style())
        self.load_payments()
        
        # PAYMENT ACTIONS
        payment_action = QHBoxLayout()
        
        self.btn_pay = QPushButton("💰 Pay Selected Bill")
        self.btn_pay.setMinimumHeight(45)
        self.btn_pay.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_pay.setStyleSheet(self._get_button_style("#27ae60"))
        self.btn_pay.clicked.connect(self.pay_selected)
        
        self.btn_details = QPushButton("📊 View Details")
        self.btn_details.setMinimumHeight(45)
        self.btn_details.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.btn_details.setStyleSheet(self._get_button_style("#3498db"))
        self.btn_details.clicked.connect(self.view_bill_details)
        
        payment_action.addWidget(self.btn_pay)
        payment_action.addWidget(self.btn_details)
        
        right_layout.addWidget(bills_label)
        right_layout.addWidget(self.payment_list)
        right_layout.addLayout(payment_action)

        # ADD COLUMNS TO CONTENT LAYOUT
        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 1)
        
        layout.addLayout(content_layout)

        self.setLayout(layout)

    def _get_input_style(self):
        """Input field styling"""
        return """
            QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                font-size: 11px;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
                background-color: #f8f9fa;
            }
        """

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
            "#e74c3c": ["#c0392b", "#a93226", "#922b21"],
            "#27ae60": ["#1e8449", "#186a3b", "#145a32"],
            "#3498db": ["#2980b9", "#1f618d", "#154360"],
        }
        return color_map.get(color, [color, color, color])[factor - 1] if factor > 0 else color

    # ─────────────────────────────
    # SUBMIT COMPLAINT
    # ─────────────────────────────
    def submit_complaint(self):
        """Submit new complaint"""
        text = self.complaint_input.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "Error", "⚠️ Please enter a complaint")
            return

        try:
            # In dev mode, show mock submission
            self.logger.info(f"Complaint submitted by {self.user['full_name']}: {text[:50]}")
            QMessageBox.information(self, "Success", "✅ Complaint submitted successfully!\nReference: #2026-05-{len(text)}")
            self.complaint_input.clear()
            self.load_recent_complaints()
        except Exception as e:
            self.logger.error(f"Error submitting complaint: {e}")
            QMessageBox.critical(self, "Error", f"Error: {str(e)[:50]}")

    # ─────────────────────────────
    # LOAD RECENT COMPLAINTS
    # ─────────────────────────────
    def load_recent_complaints(self):
        """Load recent complaints"""
        self.recent_list.clear()

        try:
            # Mock complaints for dev mode
            complaints = [
                {"id": "2026-05-001", "title": "Road pothole in Block A", "status": "Resolved"},
                {"id": "2026-05-002", "title": "Street light not working", "status": "In Progress"},
                {"id": "2026-05-003", "title": "Water supply low", "status": "Submitted"},
            ]

            for complaint in complaints:
                status_emoji = "✅" if complaint['status'] == "Resolved" else "⏳"
                item_text = f"{status_emoji} {complaint['title']}\n   Status: {complaint['status']} | Ref: {complaint['id']}"
                self.recent_list.addItem(item_text)

            self.logger.info(f"Loaded {len(complaints)} complaints")
        except Exception as e:
            self.logger.error(f"Error loading complaints: {e}")
            self.recent_list.addItem("Error loading complaints")

    # ─────────────────────────────
    # LOAD PAYMENTS
    # ─────────────────────────────
    def load_payments(self):
        """Load bills and payments"""
        self.payment_list.clear()

        try:
            # Mock bills for dev mode
            bills = [
                {"id": 1, "type": "Electricity", "amount": 2500, "status": "Pending", "due": "2026-05-15"},
                {"id": 2, "type": "Water", "amount": 800, "status": "Pending", "due": "2026-05-20"},
                {"id": 3, "type": "Gas", "amount": 1200, "status": "Paid", "due": "2026-04-30"},
            ]

            for bill in bills:
                status_emoji = "💰" if bill['status'] == "Pending" else "✅"
                item_text = f"{status_emoji} {bill['type']}: PKR {bill['amount']}\n   Status: {bill['status']} | Due: {bill['due']}"
                self.payment_list.addItem(item_text)

            self.logger.info(f"Loaded {len(bills)} bills")
        except Exception as e:
            self.logger.error(f"Error loading payments: {e}")
            self.payment_list.addItem("Error loading bills")

    # ─────────────────────────────
    # PAY SELECTED BILL
    # ─────────────────────────────
    def pay_selected(self):
        """Pay selected bill"""
        current = self.payment_list.currentItem()

        if not current:
            QMessageBox.warning(self, "Error", "Please select a bill to pay")
            return

        try:
            # Get bill info
            text = current.text()
            bill_type = text.split(":")[0].strip().replace("💰 ", "")
            amount = text.split("PKR")[1].split("\\n")[0].strip() if "PKR" in text else "Amount"

            # Generate transaction reference
            import random
            txn_id = f"TXN{random.randint(10000, 99999)}"

            # Show payment options dialog
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Payment Options")
            msg_box.setText(f"💳 Select Payment Method\n\nBill Type: {bill_type}\nAmount: PKR {amount}\nTransaction ID: {txn_id}")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Ok | 
                QMessageBox.StandardButton.Cancel
            )
            msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            
            btn_online = msg_box.addButton("🌐 Online Payment", QMessageBox.ButtonRole.ActionRole)
            btn_bank = msg_box.addButton("🏦 Bank Transfer", QMessageBox.ButtonRole.ActionRole)
            btn_check = msg_box.addButton("✏️ Check", QMessageBox.ButtonRole.ActionRole)

            result = msg_box.exec()

            if result == QMessageBox.StandardButton.Ok or msg_box.clickedButton() == btn_online:
                payment_method = "Online Payment"
            elif msg_box.clickedButton() == btn_bank:
                payment_method = "Bank Transfer"
            elif msg_box.clickedButton() == btn_check:
                payment_method = "Check"
            else:
                return

            self.logger.info(f"Payment initiated by {self.user['full_name']}: {amount} via {payment_method}")
            
            # Show success and next steps
            QMessageBox.information(
                self, 
                "Payment Submitted", 
                f"""✅ Payment Submitted Successfully!

Transaction ID: {txn_id}
Amount: PKR {amount}
Method: {payment_method}
Status: Pending Verification

📝 Your payment has been submitted to the admin for verification.
⏳ Once verified (usually within 24 hours), the bill will be marked as paid.

You will receive a notification once the payment is verified."""
            )
            
            # Remove from list after payment (simulate)
            # In real scenario, this would only be removed after admin verification
            # self.load_payments()
            
        except Exception as e:
            self.logger.error(f"Error processing payment: {e}")
            QMessageBox.critical(self, "Error", f"Error: {str(e)[:50]}")

    # ─────────────────────────────
    # VIEW BILL DETAILS
    # ─────────────────────────────
    def view_bill_details(self):
        """View bill details"""
        current = self.payment_list.currentItem()

        if not current:
            QMessageBox.warning(self, "Error", "Please select a bill")
            return

        details = """
📊 BILL DETAILS

Utility Type: Electricity
Meter Number: MET-2026-0001
Previous Reading: 5000 kWh
Current Reading: 5250 kWh
Units Consumed: 250 kWh
Rate per Unit: PKR 10
Amount Due: PKR 2500
Tax (16%): PKR 400
Total: PKR 2900

Due Date: 2026-05-15
Status: PENDING

Pay online or at nearest office.
        """
        QMessageBox.information(self, "Bill Details", details)

    # ─────────────────────────────
    # LOGOUT
    # ─────────────────────────────
    def logout(self):
        """Logout and exit"""
        self.logger.info(f"{self.user['full_name']} logged out")
        
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()