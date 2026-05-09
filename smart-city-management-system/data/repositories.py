# ============================================================
# DATA ACCESS LAYER - REPOSITORIES
# ============================================================

from core.database import db
from utils.exceptions import ResourceNotFoundException, DuplicateResourceException


class BaseRepository:
    """Base repository with common CRUD operations"""

    def __init__(self, table_name):
        self.table_name = table_name

    def get_by_id(self, id_column, id_value):
        """Get record by ID"""
        query = f"SELECT * FROM {self.table_name} WHERE {id_column} = ?"
        result = db.execute_single(query, (id_value,))
        if not result:
            raise ResourceNotFoundException(f"Record not found in {self.table_name}")
        return result

    def get_all(self, limit=None):
        """Get all records"""
        query = f"SELECT * FROM {self.table_name}"
        if limit:
            query += f" OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"
        return db.execute_query(query)

    def get_by_filter(self, column, value):
        """Get records by filter"""
        query = f"SELECT * FROM {self.table_name} WHERE {column} = ?"
        return db.execute_query(query, (value,))

    def count(self):
        """Get total record count"""
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        result = db.execute_single(query)
        return result[0] if result else 0


class CitizenRepository(BaseRepository):
    """Citizen data repository"""

    def __init__(self):
        super().__init__("citizens")

    def get_by_username(self, username):
        """Get citizen by username"""
        return self.get_by_filter("username", username)

    def get_active_citizens(self):
        """Get all active citizens"""
        query = "SELECT * FROM citizens WHERE is_active = 1"
        return db.execute_query(query)

    def create_citizen(self, username, password_hash, full_name, email, phone, cnic, address, zone):
        """Create new citizen"""
        query = """
            INSERT INTO citizens 
            (username, password_hash, full_name, email, phone, cnic, address, zone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (username, password_hash, full_name, email, phone, cnic, address, zone)
        db.execute_update(query, params)


class EmployeeRepository(BaseRepository):
    """Employee data repository"""

    def __init__(self):
        super().__init__("employees")

    def get_by_username(self, username):
        """Get employee by username"""
        return self.get_by_filter("username", username)

    def get_by_department(self, dept_id):
        """Get employees in department"""
        return self.get_by_filter("dept_id", dept_id)

    def get_active_employees(self):
        """Get all active employees"""
        query = "SELECT * FROM employees WHERE is_active = 1"
        return db.execute_query(query)


class DepartmentRepository(BaseRepository):
    """Department data repository"""

    def __init__(self):
        super().__init__("departments")

    def get_by_name(self, name):
        """Get department by name"""
        return self.get_by_filter("dept_name", name)


class ComplaintRepository(BaseRepository):
    """Complaint data repository"""

    def __init__(self):
        super().__init__("complaints")

    def get_by_citizen(self, citizen_id):
        """Get complaints by citizen"""
        return self.get_by_filter("citizen_id", citizen_id)

    def get_by_status(self, status):
        """Get complaints by status"""
        return self.get_by_filter("status", status)

    def get_pending_complaints(self):
        """Get unresolved complaints"""
        query = """
            SELECT * FROM complaints 
            WHERE status IN ('Submitted', 'Assigned', 'In Progress')
            ORDER BY submitted_at DESC
        """
        return db.execute_query(query)


class TaskRepository(BaseRepository):
    """Task data repository"""

    def __init__(self):
        super().__init__("tasks")

    def get_by_employee(self, emp_id):
        """Get tasks assigned to employee"""
        return self.get_by_filter("assigned_to", emp_id)

    def get_by_status(self, status):
        """Get tasks by status"""
        return self.get_by_filter("status", status)

    def get_pending_tasks(self):
        """Get incomplete tasks"""
        query = """
            SELECT * FROM tasks 
            WHERE status IN ('Pending', 'In Progress')
            ORDER BY due_date ASC
        """
        return db.execute_query(query)


class VehicleRepository(BaseRepository):
    """Vehicle data repository"""

    def __init__(self):
        super().__init__("vehicles")

    def get_available_vehicles(self):
        """Get available vehicles"""
        return self.get_by_filter("status", "Available")

    def get_by_department(self, dept_id):
        """Get vehicles in department"""
        return self.get_by_filter("dept_id", dept_id)


class UtilityRepository(BaseRepository):
    """Utility data repository"""

    def __init__(self):
        super().__init__("utilities")

    def get_by_citizen(self, citizen_id):
        """Get utilities for citizen"""
        return self.get_by_filter("citizen_id", citizen_id)

    def get_by_type(self, utility_type):
        """Get utilities by type"""
        return self.get_by_filter("utility_type", utility_type)


class PaymentRepository(BaseRepository):
    """Payment data repository"""

    def __init__(self):
        super().__init__("payments")

    def get_by_citizen(self, citizen_id):
        """Get payments by citizen"""
        return self.get_by_filter("citizen_id", citizen_id)

    def get_pending_payments(self):
        """Get unpaid bills"""
        return self.get_by_filter("status", "Pending")

    def get_overdue_payments(self):
        """Get overdue payments"""
        return self.get_by_filter("status", "Overdue")
