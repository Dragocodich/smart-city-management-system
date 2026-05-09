# ============================================================
# COMPLAINT MANAGEMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import ComplaintRepository, TaskRepository
from utils.helpers import DateTimeHelper


class ComplaintService:
    """Handle all complaint-related operations"""

    def __init__(self):
        self.repo = ComplaintRepository()
        self.task_repo = TaskRepository()

    def submit_complaint(self, citizen_id, dept_id, title, description, category, location, priority="Normal"):
        """Submit new complaint"""
        query = """
            INSERT INTO complaints 
            (citizen_id, dept_id, title, description, category, location, priority, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Submitted')
        """
        params = (citizen_id, dept_id, title, description, category, location, priority)
        db.execute_update(query, params)

    def get_complaint_details(self, complaint_id):
        """Get complaint details"""
        return self.repo.get_by_id("complaint_id", complaint_id)

    def update_status(self, complaint_id, status):
        """Update complaint status"""
        query = "UPDATE complaints SET status = ? WHERE complaint_id = ?"
        db.execute_update(query, (status, complaint_id))

    def assign_task(self, complaint_id, dept_id, emp_id, title, priority="Normal"):
        """Create and assign task from complaint"""
        query = """
            INSERT INTO tasks 
            (complaint_id, dept_id, assigned_to, assigned_by, title, priority, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Pending')
        """
        params = (complaint_id, dept_id, emp_id, 1, title, priority)
        db.execute_update(query, params)
        
        # Update complaint status
        self.update_status(complaint_id, "Assigned")

    def get_pending_complaints(self):
        """Get all pending complaints"""
        return self.repo.get_pending_complaints()

    def get_citizen_complaints(self, citizen_id):
        """Get complaints by specific citizen"""
        return self.repo.get_by_citizen(citizen_id)

    def rate_complaint(self, complaint_id, rating):
        """Add citizen rating to resolved complaint"""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        query = "UPDATE complaints SET citizen_rating = ? WHERE complaint_id = ?"
        db.execute_update(query, (rating, complaint_id))

    def get_statistics(self):
        """Get complaint statistics"""
        queries = {
            "total": "SELECT COUNT(*) FROM complaints",
            "pending": "SELECT COUNT(*) FROM complaints WHERE status IN ('Submitted', 'Assigned', 'In Progress')",
            "resolved": "SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'",
            "avg_rating": "SELECT AVG(citizen_rating) FROM complaints WHERE citizen_rating IS NOT NULL"
        }
        
        stats = {}
        for key, query in queries.items():
            result = db.execute_single(query)
            stats[key] = result[0] if result else 0
        
        return stats
