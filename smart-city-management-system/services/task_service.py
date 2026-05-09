# ============================================================
# TASK MANAGEMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import TaskRepository


class TaskService:
    """Handle task assignment and management"""

    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, complaint_id, dept_id, assigned_to, title, description, priority="Normal"):
        """Create new task"""
        query = """
            INSERT INTO tasks 
            (complaint_id, dept_id, assigned_to, assigned_by, title, description, priority, status)
            VALUES (?, ?, ?, 1, ?, ?, ?, 'Pending')
        """
        params = (complaint_id, dept_id, assigned_to, title, description, priority)
        db.execute_update(query, params)

    def get_employee_tasks(self, emp_id):
        """Get all tasks for employee"""
        return self.repo.get_by_employee(emp_id)

    def get_pending_tasks(self):
        """Get all pending tasks"""
        return self.repo.get_pending_tasks()

    def update_task_status(self, task_id, status):
        """Update task status"""
        query = "UPDATE tasks SET status = ? WHERE task_id = ?"
        db.execute_update(query, (status, task_id))

    def start_task(self, task_id):
        """Mark task as in progress"""
        self.update_task_status(task_id, "In Progress")

    def complete_task(self, task_id):
        """Mark task as completed"""
        query = """
            UPDATE tasks
            SET status = 'Completed', completed_at = GETDATE()
            WHERE task_id = ?
        """
        db.execute_update(query, (task_id,))

    def reassign_task(self, task_id, new_emp_id):
        """Reassign task to different employee"""
        query = "UPDATE tasks SET assigned_to = ? WHERE task_id = ?"
        db.execute_update(query, (new_emp_id, task_id))

    def extend_due_date(self, task_id, new_due_date):
        """Extend task due date"""
        query = "UPDATE tasks SET due_date = ? WHERE task_id = ?"
        db.execute_update(query, (new_due_date, task_id))

    def get_overdue_tasks(self):
        """Get tasks past due date"""
        query = """
            SELECT * FROM tasks
            WHERE status != 'Completed' AND due_date < GETDATE()
            ORDER BY due_date ASC
        """
        return db.execute_query(query)

    def get_task_statistics(self):
        """Get task statistics"""
        queries = {
            "total_tasks": "SELECT COUNT(*) FROM tasks",
            "pending": "SELECT COUNT(*) FROM tasks WHERE status = 'Pending'",
            "in_progress": "SELECT COUNT(*) FROM tasks WHERE status = 'In Progress'",
            "completed": "SELECT COUNT(*) FROM tasks WHERE status = 'Completed'",
            "overdue": "SELECT COUNT(*) FROM tasks WHERE status != 'Completed' AND due_date < GETDATE()"
        }
        
        stats = {}
        for key, query in queries.items():
            result = db.execute_single(query)
            stats[key] = result[0] if result else 0
        
        return stats

    def get_employee_performance(self, emp_id):
        """Get employee task completion metrics"""
        query = """
            SELECT 
                COUNT(*) as total_assigned,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
                AVG(DATEDIFF(DAY, created_at, ISNULL(completed_at, GETDATE()))) as avg_days_to_complete
            FROM tasks
            WHERE assigned_to = ?
        """
        return db.execute_single(query, (emp_id,))
