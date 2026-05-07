from PyQt6.QtWidgets import *
from db import db


class CitizenPanel(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user["data"]

        self.setWindowTitle("Citizen Dashboard")
        self.setGeometry(300, 200, 500, 450)

        layout = QVBoxLayout()

        # ───── COMPLAINT INPUT ─────
        self.complaint_input = QLineEdit()
        self.complaint_input.setPlaceholderText(
            "Enter complaint"
        )

        submit_btn = QPushButton("Submit Complaint")
        submit_btn.clicked.connect(
            self.submit_complaint
        )

        # ───── PAYMENT LIST ─────
        self.payment_list = QListWidget()

        self.load_payments()

        pay_btn = QPushButton("Pay Selected Bill")
        pay_btn.clicked.connect(
            self.pay_selected
        )

        # ───── UI ─────
        layout.addWidget(
            QLabel(f"Welcome {self.user['full_name']}")
        )

        layout.addWidget(self.complaint_input)
        layout.addWidget(submit_btn)

        layout.addWidget(QLabel("Your Bills:"))
        layout.addWidget(self.payment_list)
        layout.addWidget(pay_btn)

        self.setLayout(layout)

    # ─────────────────────────────
    # SUBMIT COMPLAINT
    # ─────────────────────────────
    def submit_complaint(self):

        text = self.complaint_input.text().strip()

        if not text:

            QMessageBox.warning(
                self,
                "Error",
                "Complaint cannot be empty"
            )

            return

        db.add_complaint(
            self.user["citizen_id"],
            1,
            text,
            "User complaint",
            "General",
            "Normal",
            "Karachi"
        )

        QMessageBox.information(
            self,
            "Success",
            "Complaint Submitted"
        )

        self.complaint_input.clear()

    # ─────────────────────────────
    # LOAD PAYMENTS
    # ─────────────────────────────
    def load_payments(self):

        self.payment_list.clear()

        payments = db.get_payments(
            self.user["citizen_id"]
        )

        for p in payments:

            self.payment_list.addItem(
                f"ID:{p['payment_id']} - "
                f"{p['payment_type']} - "
                f"{p['status']}"
            )

    # ─────────────────────────────
    # PAY BILL
    # ─────────────────────────────
    def pay_selected(self):

        item = self.payment_list.currentItem()

        if item:

            pid = int(
                item.text().split()[0].split(":")[1]
            )

            db.pay_bill(pid)

            QMessageBox.information(
                self,
                "Paid",
                "Payment Done"
            )

            self.load_payments()