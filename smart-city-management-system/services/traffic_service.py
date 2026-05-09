# ============================================================
# TRAFFIC MANAGEMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import BaseRepository


class TrafficService:
    """Handle traffic management operations"""

    def __init__(self):
        self.sensor_repo = BaseRepository("sensors")
        self.traffic_repo = BaseRepository("traffic_data")

    def record_traffic_data(self, sensor_id, intersection, zone, vehicle_count, congestion_level):
        """Record traffic sensor data"""
        query = """
            INSERT INTO traffic_data 
            (sensor_id, intersection, zone, vehicle_count, congestion_level)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (sensor_id, intersection, zone, vehicle_count, congestion_level)
        db.execute_update(query, params)

    def get_congestion_level(self, zone):
        """Get current congestion level for zone"""
        query = """
            SELECT TOP 1 congestion_level, vehicle_count
            FROM traffic_data
            WHERE zone = ?
            ORDER BY recorded_at DESC
        """
        return db.execute_single(query, (zone,))

    def analyze_traffic_pattern(self, zone, hours=24):
        """Analyze traffic patterns over time"""
        query = """
            SELECT recorded_at, vehicle_count, congestion_level
            FROM traffic_data
            WHERE zone = ? AND recorded_at > DATEADD(hour, -?, GETDATE())
            ORDER BY recorded_at DESC
        """
        return db.execute_query(query, (zone, hours))

    def adjust_signal_timing(self, data_id, timing_ns, timing_ew):
        """Adjust traffic signal timing"""
        query = """
            UPDATE traffic_data 
            SET signal_timing_ns = ?, signal_timing_ew = ?
            WHERE data_id = ?
        """
        db.execute_update(query, (timing_ns, timing_ew, data_id))

    def get_all_sensors(self):
        """Get all traffic sensors"""
        return self.sensor_repo.get_all()

    def get_sensors_by_zone(self, zone):
        """Get sensors in specific zone"""
        return self.sensor_repo.get_by_filter("zone", zone)

    def register_sensor(self, sensor_type, location, zone, latitude, longitude):
        """Register new traffic sensor"""
        query = """
            INSERT INTO sensors 
            (sensor_type, location, zone, latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?, 'Active')
        """
        params = (sensor_type, location, zone, latitude, longitude)
        db.execute_update(query, params)

    def get_traffic_alerts(self):
        """Get areas with critical congestion"""
        query = """
            SELECT TOP 1 intersection, zone, vehicle_count, congestion_level, recorded_at
            FROM traffic_data
            WHERE congestion_level = 'Critical'
            ORDER BY recorded_at DESC
        """
        return db.execute_query(query)

    def get_traffic_statistics(self):
        """Get traffic system statistics"""
        queries = {
            "total_sensors": "SELECT COUNT(*) FROM sensors WHERE status = 'Active'",
            "critical_zones": "SELECT COUNT(DISTINCT zone) FROM traffic_data WHERE congestion_level = 'Critical'",
            "avg_vehicles": "SELECT AVG(vehicle_count) FROM traffic_data",
        }
        
        stats = {}
        for key, query in queries.items():
            result = db.execute_single(query)
            stats[key] = result[0] if result else 0
        
        return stats
