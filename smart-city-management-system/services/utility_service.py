# ============================================================
# UTILITY MANAGEMENT SERVICE
# ============================================================

from core.database import db
from data.repositories import UtilityRepository
from decimal import Decimal


class UtilityService:
    """Handle utility management (electricity, water, gas)"""

    def __init__(self):
        self.repo = UtilityRepository()

    def record_meter_reading(self, citizen_id, utility_type, meter_no, current_reading):
        """Record new meter reading"""
        # Get previous reading
        query = """
            SELECT utility_id, curr_reading, rate_per_unit
            FROM utilities
            WHERE citizen_id = ? AND utility_type = ? AND meter_no = ?
            ORDER BY reading_date DESC
        """
        prev = db.execute_single(query, (citizen_id, utility_type, meter_no))
        
        prev_reading = prev[1] if prev else 0
        units_consumed = current_reading - prev_reading
        rate = prev[2] if prev else self._get_default_rate(utility_type)

        # Insert new reading
        insert_query = """
            INSERT INTO utilities 
            (citizen_id, utility_type, meter_no, prev_reading, curr_reading, units_consumed, rate_per_unit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db.execute_update(insert_query, (
            citizen_id, utility_type, meter_no, prev_reading, 
            current_reading, units_consumed, rate
        ))

    def _get_default_rate(self, utility_type):
        """Get default rate for utility type"""
        rates = {
            "Electricity": 12.50,
            "Water": 25.00,
            "Gas": 8.75
        }
        return rates.get(utility_type, 0)

    def get_citizen_utilities(self, citizen_id):
        """Get all utilities for citizen"""
        return self.repo.get_by_citizen(citizen_id)

    def get_utility_readings(self, citizen_id, utility_type):
        """Get readings history for specific utility"""
        query = """
            SELECT reading_date, prev_reading, curr_reading, units_consumed
            FROM utilities
            WHERE citizen_id = ? AND utility_type = ?
            ORDER BY reading_date DESC
        """
        return db.execute_query(query, (citizen_id, utility_type))

    def monitor_consumption(self, citizen_id):
        """Monitor citizen's utility consumption"""
        query = """
            SELECT utility_type, SUM(units_consumed) as total_consumption, AVG(units_consumed) as avg_consumption
            FROM utilities
            WHERE citizen_id = ?
            GROUP BY utility_type
        """
        return db.execute_query(query, (citizen_id,))

    def get_zone_consumption(self, zone):
        """Get total consumption for zone"""
        query = """
            SELECT utility_type, SUM(units_consumed) as total, AVG(units_consumed) as average
            FROM utilities
            WHERE zone = ?
            GROUP BY utility_type
        """
        return db.execute_query(query, (zone,))

    def get_high_consumers(self, utility_type, threshold=1000):
        """Get citizens with high consumption"""
        query = """
            SELECT TOP 10 c.citizen_id, c.full_name, SUM(u.units_consumed) as total_consumption
            FROM citizens c
            JOIN utilities u ON c.citizen_id = u.citizen_id
            WHERE u.utility_type = ? AND u.units_consumed > ?
            GROUP BY c.citizen_id, c.full_name
            ORDER BY total_consumption DESC
        """
        return db.execute_query(query, (utility_type, threshold))

    def get_utility_statistics(self):
        """Get utility system statistics"""
        queries = {
            "total_connections": "SELECT COUNT(DISTINCT citizen_id) FROM utilities",
            "electricity_consumption": "SELECT SUM(units_consumed) FROM utilities WHERE utility_type = 'Electricity'",
            "water_consumption": "SELECT SUM(units_consumed) FROM utilities WHERE utility_type = 'Water'",
            "gas_consumption": "SELECT SUM(units_consumed) FROM utilities WHERE utility_type = 'Gas'"
        }
        
        stats = {}
        for key, query in queries.items():
            result = db.execute_single(query)
            stats[key] = float(result[0]) if result and result[0] else 0
        
        return stats
