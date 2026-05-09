# ============================================================
# USER MANAGEMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import EmployeeRepository, CitizenRepository
from utils.exceptions import DuplicateResourceException


class UserManagementService:
    """Handle user account management"""

    def __init__(self):
        self.employee_repo = EmployeeRepository()
        self.citizen_repo = CitizenRepository()

    def create_employee(self, username, password, full_name, dept_id, role, email, phone, address):
        """Create new employee account"""
        # Check if username exists
        existing = self.employee_repo.get_by_username(username)
        if existing:
            raise DuplicateResourceException(f"Username '{username}' already exists")

        password_hash = db.hash_password(password)
        query = """
            INSERT INTO employees 
            (username, password_hash, full_name, dept_id, role, email, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (username, password_hash, full_name, dept_id, role, email, phone, address)
        db.execute_update(query, params)

    def create_citizen(self, username, password, full_name, email, phone, cnic, address, zone):
        """Create new citizen account"""
        # Check if username exists
        existing = self.citizen_repo.get_by_username(username)
        if existing:
            raise DuplicateResourceException(f"Username '{username}' already exists")

        password_hash = db.hash_password(password)
        self.citizen_repo.create_citizen(
            username, password_hash, full_name, email, phone, cnic, address, zone
        )

    def update_employee_profile(self, emp_id, full_name=None, email=None, phone=None, address=None):
        """Update employee profile"""
        updates = []
        params = []

        if full_name:
            updates.append("full_name = ?")
            params.append(full_name)
        if email:
            updates.append("email = ?")
            params.append(email)
        if phone:
            updates.append("phone = ?")
            params.append(phone)
        if address:
            updates.append("address = ?")
            params.append(address)

        if not updates:
            return

        params.append(emp_id)
        query = f"UPDATE employees SET {', '.join(updates)} WHERE emp_id = ?"
        db.execute_update(query, tuple(params))

    def update_citizen_profile(self, citizen_id, full_name=None, email=None, phone=None, address=None, zone=None):
        """Update citizen profile"""
        updates = []
        params = []

        if full_name:
            updates.append("full_name = ?")
            params.append(full_name)
        if email:
            updates.append("email = ?")
            params.append(email)
        if phone:
            updates.append("phone = ?")
            params.append(phone)
        if address:
            updates.append("address = ?")
            params.append(address)
        if zone:
            updates.append("zone = ?")
            params.append(zone)

        if not updates:
            return

        params.append(citizen_id)
        query = f"UPDATE citizens SET {', '.join(updates)} WHERE citizen_id = ?"
        db.execute_update(query, tuple(params))

    def change_password(self, user_type, user_id, old_password, new_password):
        """Change user password"""
        # Verify old password
        if user_type == "employee":
            query = "SELECT password_hash FROM employees WHERE emp_id = ?"
        else:
            query = "SELECT password_hash FROM citizens WHERE citizen_id = ?"

        result = db.execute_single(query, (user_id,))
        if not result or not db.verify_password(old_password, result[0]):
            raise Exception("Current password is incorrect")

        # Update password
        new_hash = db.hash_password(new_password)
        if user_type == "employee":
            update_query = "UPDATE employees SET password_hash = ? WHERE emp_id = ?"
        else:
            update_query = "UPDATE citizens SET password_hash = ? WHERE citizen_id = ?"

        db.execute_update(update_query, (new_hash, user_id))

    def deactivate_user(self, user_type, user_id):
        """Deactivate user account"""
        if user_type == "employee":
            query = "UPDATE employees SET is_active = 0 WHERE emp_id = ?"
        else:
            query = "UPDATE citizens SET is_active = 0 WHERE citizen_id = ?"

        db.execute_update(query, (user_id,))

    def activate_user(self, user_type, user_id):
        """ Activate user account"""
        if user_type == "employee":
            query = "UPDATE employees SET is_active = 1 WHERE emp_id = ?"
        else:
            query = "UPDATE citizens SET is_active = 1 WHERE citizen_id = ?"

        db.execute_update(query, (user_id,))

    def record_login(self, user_type, user_id):
        """Record user login"""
        if user_type == "employee":
            query = "UPDATE employees SET last_login = GETDATE() WHERE emp_id = ?"
        else:
            # Citizens don't have last_login, but you can add it if needed
            pass

        if user_type == "employee":
            db.execute_update(query, (user_id,))
