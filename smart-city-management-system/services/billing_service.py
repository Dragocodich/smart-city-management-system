# ============================================================
# BILLING AND PAYMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import PaymentRepository, UtilityRepository
from utils.helpers import DateTimeHelper
from decimal import Decimal


class BillingService:
    """Handle billing and payment operations"""

    def __init__(self):
        self.payment_repo = PaymentRepository()
        self.utility_repo = UtilityRepository()

    def generate_bill(self, citizen_id, utility_id, amount, tax_rate=0.15, bill_month=None):
        """Generate utility bill"""
        tax_amount = amount * Decimal(tax_rate)
        total_amount = amount + tax_amount
        
        if not bill_month:
            bill_month = DateTimeHelper.now().strftime("%Y-%m")

        query = """
            INSERT INTO payments 
            (citizen_id, utility_id, payment_type, amount, tax_amount, total_amount, status, bill_month, due_date)
            VALUES (?, ?, 'Utility Bill', ?, ?, ?, 'Pending', ?, DATEADD(day, 15, GETDATE()))
        """
        params = (citizen_id, utility_id, amount, tax_amount, total_amount, bill_month)
        db.execute_update(query, params)

    def process_payment(self, payment_id, payment_method, transaction_ref):
        """Process payment"""
        query = """
            UPDATE payments
            SET status = 'Paid', paid_at = GETDATE(), payment_method = ?, transaction_ref = ?
            WHERE payment_id = ?
        """
        db.execute_update(query, (payment_method, transaction_ref, payment_id))

    def get_pending_bills(self, citizen_id):
        """Get citizen's pending bills"""
        query = """
            SELECT * FROM payments
            WHERE citizen_id = ? AND status IN ('Pending', 'Overdue')
            ORDER BY due_date ASC
        """
        return db.execute_query(query, (citizen_id,))

    def get_payment_history(self, citizen_id):
        """Get citizen's payment history"""
        query = """
            SELECT * FROM payments
            WHERE citizen_id = ?
            ORDER BY created_at DESC
        """
        return db.execute_query(query, (citizen_id,))

    def check_overdue_payments(self):
        """Mark overdue payments"""
        query = """
            UPDATE payments
            SET status = 'Overdue'
            WHERE status = 'Pending' AND due_date < GETDATE()
        """
        db.execute_update(query)

    def get_bill_statistics(self):
        """Get billing statistics"""
        queries = {
            "total_bills": "SELECT COUNT(*) FROM payments",
            "paid_bills": "SELECT COUNT(*) FROM payments WHERE status = 'Paid'",
            "pending_bills": "SELECT COUNT(*) FROM payments WHERE status = 'Pending'",
            "overdue_bills": "SELECT COUNT(*) FROM payments WHERE status = 'Overdue'",
            "total_revenue": "SELECT SUM(total_amount) FROM payments WHERE status = 'Paid'",
            "pending_amount": "SELECT SUM(total_amount) FROM payments WHERE status IN ('Pending', 'Overdue')"
        }
        
        stats = {}
        for key, query in queries.items():
            result = db.execute_single(query)
            stats[key] = float(result[0]) if result and result[0] else 0
        
        return stats

    def generate_bill_to_citizen(self, citizen_id):
        """Auto-generate monthly bills for citizen"""
        # Get all utilities
        utilities = self.utility_repo.get_by_citizen(citizen_id)
        
        for utility in utilities:
            # Get latest reading
            reading_query = """
                SELECT units_consumed, rate_per_unit FROM utilities
                WHERE citizen_id = ? AND utility_id = ?
                ORDER BY reading_date DESC
            """
            reading = db.execute_single(reading_query, (citizen_id, utility[0]))
            
            if reading:
                amount = Decimal(reading[0]) * Decimal(reading[1])
                self.generate_bill(citizen_id, utility[0], amount)

    def send_payment_reminder(self, days_before_due=3):
        """Get bills that need reminder"""
        query = """
            SELECT * FROM payments
            WHERE status = 'Pending' 
            AND due_date BETWEEN GETDATE() AND DATEADD(day, ?, GETDATE())
        """
        return db.execute_query(query, (days_before_due,))
