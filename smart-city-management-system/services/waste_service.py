# ============================================================
# WASTE MANAGEMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import VehicleRepository, BaseRepository


class WasteService:
    """Handle waste management operations"""

    def __init__(self):
        self.vehicle_repo = VehicleRepository()
        self.waste_repo = BaseRepository("waste_collection")

    def schedule_collection(self, vehicle_id, zone, route_info, scheduled_time):
        """Schedule waste collection"""
        query = """
            INSERT INTO waste_collection 
            (vehicle_id, zone, route_info, status, scheduled_at)
            VALUES (?, ?, ?, 'Scheduled', ?)
        """
        params = (vehicle_id, zone, route_info, scheduled_time)
        db.execute_update(query, params)

    def start_collection(self, collection_id):
        """Start collection route"""
        query = "UPDATE waste_collection SET status = 'In Progress' WHERE collection_id = ?"
        db.execute_update(query, (collection_id,))

    def complete_collection(self, collection_id, bins_collected, weight_kg):
        """Mark collection as completed"""
        query = """
            UPDATE waste_collection 
            SET status = 'Completed', bins_collected = ?, weight_kg = ?, completed_at = GETDATE()
            WHERE collection_id = ?
        """
        db.execute_update(query, (bins_collected, weight_kg, collection_id))

    def get_scheduled_collections(self, zone=None):
        """Get scheduled collections"""
        if zone:
            query = """
                SELECT * FROM waste_collection 
                WHERE status = 'Scheduled' AND zone = ?
                ORDER BY scheduled_at ASC
            """
            return db.execute_query(query, (zone,))
        else:
            query = """
                SELECT * FROM waste_collection 
                WHERE status = 'Scheduled'
                ORDER BY scheduled_at ASC
            """
            return db.execute_query(query)

    def optimize_route(self, zone):
        """Get optimized collection route for zone"""
        query = """
            SELECT collection_id, zone, route_info, bins_collected
            FROM waste_collection
            WHERE zone = ? AND status IN ('Scheduled', 'In Progress')
            ORDER BY scheduled_at ASC
        """
        return db.execute_query(query, (zone,))

    def get_available_vehicles(self):
        """Get available waste collection vehicles"""
        return self.vehicle_repo.get_available_vehicles()

    def register_vehicle(self, dept_id, vehicle_no, vehicle_type, capacity_kg, driver_name, driver_phone):
        """Register new vehicle"""
        query = """
            INSERT INTO vehicles 
            (dept_id, vehicle_no, vehicle_type, capacity_kg, driver_name, driver_phone, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Available')
        """
        params = (dept_id, vehicle_no, vehicle_type, capacity_kg, driver_name, driver_phone)
        db.execute_update(query, params)

    def get_waste_statistics(self):
        """Get waste management statistics"""
        queries = {
            "total_collections": "SELECT COUNT(*) FROM waste_collection",
            "completed_today": """
                SELECT COUNT(*) FROM waste_collection 
                WHERE status = 'Completed' AND CAST(completed_at AS DATE) = CAST(GETDATE() AS DATE)
            """,
            "total_weight": "SELECT SUM(weight_kg) FROM waste_collection WHERE status = 'Completed'",
            "active_vehicles": "SELECT COUNT(*) FROM vehicles WHERE status != 'Maintenance'"
        }
        
        stats = {}
        for key, query in queries.items():
            result = db.execute_single(query)
            stats[key] = result[0] if result else 0
        
        return stats
