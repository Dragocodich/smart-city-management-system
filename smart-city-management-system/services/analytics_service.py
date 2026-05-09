# ============================================================
# ANALYTICS AND REPORTING SERVICE
# ============================================================

from core.database import db
from utils.helpers import DateTimeHelper
from decimal import Decimal


class AnalyticsService:
    """Generate analytics and reports"""

    def __init__(self):
        pass

    def get_dashboard_summary(self):
        """Get overall system summary"""
        return {
            "complaints": self._get_complaint_summary(),
            "tasks": self._get_task_summary(),
            "traffic": self._get_traffic_summary(),
            "waste": self._get_waste_summary(),
            "billing": self._get_billing_summary(),
            "incidents": self._get_incident_summary()
        }

    def _get_complaint_summary(self):
        """Get complaint summary"""
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Submitted' THEN 1 ELSE 0 END) as new,
                SUM(CASE WHEN status IN ('In Progress', 'Assigned') THEN 1 ELSE 0 END) as processing,
                SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved,
                AVG(CAST(citizen_rating AS FLOAT)) as avg_rating
            FROM complaints
            WHERE submitted_at > DATEADD(MONTH, -1, GETDATE())
        """
        result = db.execute_single(query)
        return {
            "total": result[0],
            "new": result[1],
            "processing": result[2],
            "resolved": result[3],
            "avg_rating": float(result[4]) if result[4] else 0
        }

    def _get_task_summary(self):
        """Get task summary"""
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) as progress,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed
            FROM tasks
        """
        result = db.execute_single(query)
        return {
            "total": result[0],
            "pending": result[1],
            "progress": result[2],
            "completed": result[3]
        }

    def _get_traffic_summary(self):
        """Get traffic summary"""
        query = """
            SELECT 
                COUNT(DISTINCT zone) as zones,
                COUNT(CASE WHEN congestion_level = 'Critical' THEN 1 END) as critical_areas,
                COUNT(CASE WHEN congestion_level = 'High' THEN 1 END) as high_areas,
                AVG(vehicle_count) as avg_vehicles
            FROM traffic_data
            WHERE recorded_at > DATEADD(HOUR, -1, GETDATE())
        """
        result = db.execute_single(query)
        return {
            "zones": result[0],
            "critical": result[1],
            "high": result[2],
            "avg_vehicles": result[3]
        }

    def _get_waste_summary(self):
        """Get waste collection summary"""
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(weight_kg) as total_weight
            FROM waste_collection
            WHERE scheduled_at > DATEADD(DAY, -1, GETDATE())
        """
        result = db.execute_single(query)
        return {
            "total": result[0],
            "completed": result[1],
            "weight": float(result[2]) if result[2] else 0
        }

    def _get_billing_summary(self):
        """Get billing summary"""
        query = """
            SELECT 
                COUNT(*) as total_bills,
                SUM(CASE WHEN status = 'Paid' THEN 1 ELSE 0 END) as paid,
                SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'Overdue' THEN 1 ELSE 0 END) as overdue,
                SUM(CASE WHEN status = 'Paid' THEN total_amount ELSE 0 END) as revenue
            FROM payments
            WHERE created_at > DATEADD(MONTH, -1, GETDATE())
        """
        result = db.execute_single(query)
        return {
            "total": result[0],
            "paid": result[1],
            "pending": result[2],
            "overdue": result[3],
            "revenue": float(result[4]) if result[4] else 0
        }

    def _get_incident_summary(self):
        """Get incident summary"""
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status IN ('Open', 'Assigned', 'Responding') THEN 1 ELSE 0 END) as open,
                SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) as critical
            FROM incidents
            WHERE reported_at > DATEADD(MONTH, -1, GETDATE())
        """
        result = db.execute_single(query)
        return {
            "total": result[0],
            "open": result[1],
            "critical": result[2]
        }

    def get_performance_report(self, start_date, end_date):
        """Get system performance report"""
        return {
            "complaints_resolved": self._count_resolved_complaints(start_date, end_date),
            "tasks_completed": self._count_completed_tasks(start_date, end_date),
            "revenue_collected": self._get_revenue(start_date, end_date),
            "waste_collected": self._get_waste_collected(start_date, end_date),
            "incidents_handled": self._count_resolved_incidents(start_date, end_date)
        }

    def _count_resolved_complaints(self, start, end):
        """Count resolved complaints in period"""
        query = "SELECT COUNT(*) FROM complaints WHERE status = 'Resolved' AND resolved_at BETWEEN ? AND ?"
        result = db.execute_single(query, (start, end))
        return result[0]

    def _count_completed_tasks(self, start, end):
        """Count completed tasks in period"""
        query = "SELECT COUNT(*) FROM tasks WHERE status = 'Completed' AND completed_at BETWEEN ? AND ?"
        result = db.execute_single(query, (start, end))
        return result[0]

    def _get_revenue(self, start, end):
        """Get revenue in period"""
        query = "SELECT SUM(total_amount) FROM payments WHERE status = 'Paid' AND paid_at BETWEEN ? AND ?"
        result = db.execute_single(query, (start, end))
        return float(result[0]) if result and result[0] else 0

    def _get_waste_collected(self, start, end):
        """Get waste collected in period"""
        query = "SELECT SUM(weight_kg) FROM waste_collection WHERE status = 'Completed' AND completed_at BETWEEN ? AND ?"
        result = db.execute_single(query, (start, end))
        return float(result[0]) if result and result[0] else 0

    def _count_resolved_incidents(self, start, end):
        """Count resolved incidents in period"""
        query = "SELECT COUNT(*) FROM incidents WHERE status = 'Resolved' AND resolved_at BETWEEN ? AND ?"
        result = db.execute_single(query, (start, end))
        return result[0]

    def get_department_performance(self, dept_id, start_date, end_date):
        """Get department performance metrics"""
        return {
            "complaints_handled": self._count_dept_complaints(dept_id, start_date, end_date),
            "tasks_completed": self._count_dept_tasks(dept_id, start_date, end_date),
            "avg_resolution_time": self._avg_resolution_time(dept_id, start_date, end_date)
        }

    def _count_dept_complaints(self, dept_id, start, end):
        """Count complaints handled by department"""
        query = """
            SELECT COUNT(*) FROM complaints 
            WHERE dept_id = ? AND submitted_at BETWEEN ? AND ?
        """
        result = db.execute_single(query, (dept_id, start, end))
        return result[0]

    def _count_dept_tasks(self, dept_id, start, end):
        """Count tasks for department"""
        query = """
            SELECT COUNT(*) FROM tasks 
            WHERE dept_id = ? AND status = 'Completed' AND completed_at BETWEEN ? AND ?
        """
        result = db.execute_single(query, (dept_id, start, end))
        return result[0]

    def _avg_resolution_time(self, dept_id, start, end):
        """Average resolution time for department"""
        query = """
            SELECT AVG(DATEDIFF(HOUR, submitted_at, resolved_at))
            FROM complaints
            WHERE dept_id = ? AND status = 'Resolved' AND resolved_at BETWEEN ? AND ?
        """
        result = db.execute_single(query, (dept_id, start, end))
        return float(result[0]) if result and result[0] else 0
