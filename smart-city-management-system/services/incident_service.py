# ============================================================
# EMERGENCY AND INCIDENT MANAGEMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import BaseRepository
from utils.helpers import DateTimeHelper


class IncidentService:
    """Handle emergency incidents and alerts"""

    def __init__(self):
        self.incident_repo = BaseRepository("incidents")
        self.alert_repo = BaseRepository("alerts")

    def report_incident(self, reported_by, dept_id, incident_type, title, description, 
                       severity, location, latitude=None, longitude=None):
        """Report new incident"""
        query = """
            INSERT INTO incidents 
            (reported_by, dept_id, incident_type, title, description, severity, location, latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Open')
        """
        params = (reported_by, dept_id, incident_type, title, description, severity, location, latitude, longitude)
        db.execute_update(query, params)

    def get_open_incidents(self):
        """Get all open incidents"""
        query = """
            SELECT * FROM incidents
            WHERE status IN ('Open', 'Assigned', 'Responding')
            ORDER BY reported_at DESC
        """
        return db.execute_query(query)

    def get_incident_by_severity(self, severity):
        """Get incidents by severity"""
        query = """
            SELECT * FROM incidents
            WHERE severity = ? AND status != 'Closed'
            ORDER BY reported_at DESC
        """
        return db.execute_query(query, (severity,))

    def update_incident_status(self, incident_id, status):
        """Update incident status"""
        query = "UPDATE incidents SET status = ? WHERE incident_id = ?"
        db.execute_update(query, (status, incident_id))

    def resolve_incident(self, incident_id):
        """Mark incident as resolved"""
        query = """
            UPDATE incidents
            SET status = 'Resolved', resolved_at = GETDATE()
            WHERE incident_id = ?
        """
        db.execute_update(query, (incident_id,))

    def create_alert(self, alert_type, title, message, severity="Info", target_role=None, expires_hours=24):
        """Create system alert"""
        query = """
            INSERT INTO alerts 
            (alert_type, title, message, severity, target_role, expires_at)
            VALUES (?, ?, ?, ?, ?, DATEADD(hour, ?, GETDATE()))
        """
        params = (alert_type, title, message, severity, target_role, expires_hours)
        db.execute_update(query, params)

    def get_active_alerts(self):
        """Get active alerts"""
        query = """
            SELECT * FROM alerts
            WHERE is_read = 0 AND expires_at > GETDATE()
            ORDER BY created_at DESC
        """
        return db.execute_query(query)

    def get_alerts_by_role(self, role):
        """Get alerts for specific role"""
        query = """
            SELECT * FROM alerts
            WHERE (target_role = ? OR target_role IS NULL) AND expires_at > GETDATE()
            ORDER BY created_at DESC
        """
        return db.execute_query(query, (role,))

    def mark_alert_read(self, alert_id):
        """Mark alert as read"""
        query = "UPDATE alerts SET is_read = 1 WHERE alert_id = ?"
        db.execute_update(query, (alert_id,))

    def get_incident_statistics(self):
        """Get incident statistics"""
        queries = {
            "total_incidents": "SELECT COUNT(*) FROM incidents",
            "open_incidents": "SELECT COUNT(*) FROM incidents WHERE status IN ('Open', 'Assigned', 'Responding')",
            "critical": "SELECT COUNT(*) FROM incidents WHERE severity = 'Critical'",
            "resolved_today": """
                SELECT COUNT(*) FROM incidents 
                WHERE status = 'Resolved' AND CAST(resolved_at AS DATE) = CAST(GETDATE() AS DATE)
            """
        }
        
        stats = {}
        for key, query in queries.items():
            result = db.execute_single(query)
            stats[key] = result[0] if result else 0
        
        return stats

    def get_incident_response_time(self, incident_id):
        """Calculate response time for incident"""
        query = """
            SELECT 
                reported_at, resolved_at,
                DATEDIFF(MINUTE, reported_at, ISNULL(resolved_at, GETDATE())) as minutes_to_resolve
            FROM incidents
            WHERE incident_id = ?
        """
        return db.execute_single(query, (incident_id,))
