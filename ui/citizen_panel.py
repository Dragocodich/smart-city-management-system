from PyQt6.QtWidgets import *
from db import add_complaint, get_payments, pay_bill

class CitizenPanel(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user["data"]

        self.setWindowTitle("Citizen Dashboard")
        self.setGeometry(300, 200, 500, 400)

        layout = QVBoxLayout()

        self.complaint_input = QLineEdit()
        self.complaint_input.setPlaceholderText("Enter complaint")

        btn = QPushButton("Submit Complaint")
        btn.clicked.connect(self.submit_complaint)

        self.payment_list = QListWidget()
        self.load_payments()

        pay_btn = QPushButton("Pay Selected Bill")
        pay_btn.clicked.connect(self.pay_selected)

        layout.addWidget(self.complaint_input)
        layout.addWidget(btn)
        layout.addWidget(QLabel("Your Bills:"))
        layout.addWidget(self.payment_list)
        layout.addWidget(pay_btn)

        self.setLayout(layout)

    def submit_complaint(self):
        add_complaint(
            self.user["citizen_id"],
            1,
            self.complaint_input.text(),
            "User complaint",
            "General",
            "Normal",
            "Karachi"
        )
        QMessageBox.information(self, "Success", "Complaint Submitted")

    def load_payments(self):
        payments = get_payments(self.user["citizen_id"])
        for p in payments:
            self.payment_list.addItem(
                f"ID:{p['payment_id']} - {p['payment_type']} - {p['status']}"
            )

    def pay_selected(self):
        item = self.payment_list.currentItem()
        if item:
            pid = int(item.text().split()[0].split(":")[1])
            pay_bill(pid)
            QMessageBox.information(self, "Paid", "Payment Done")