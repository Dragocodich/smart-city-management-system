# ============================================================
# HELPER FUNCTIONS
# ============================================================

from datetime import datetime, timedelta
import json

class DateTimeHelper:
    """DateTime utility functions"""

    @staticmethod
    def now():
        """Get current datetime"""
        return datetime.now()

    @staticmethod
    def today():
        """Get current date"""
        return datetime.now().date()

    @staticmethod
    def add_days(days):
        """Add days to current date"""
        return datetime.now() + timedelta(days=days)

    @staticmethod
    def get_month_start():
        """Get first day of current month"""
        today = datetime.now().date()
        return today.replace(day=1)

    @staticmethod
    def get_month_end():
        """Get last day of current month"""
        today = datetime.now().date()
        if today.month == 12:
            return today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        return today.replace(month=today.month + 1, day=1) - timedelta(days=1)


class StringHelper:
    """String utility functions"""

    @staticmethod
    def truncate(text, length=50):
        """Truncate string to specified length"""
        return (text[:length] + '...') if len(text) > length else text

    @staticmethod
    def capitalize_first(text):
        """Capitalize first letter of string"""
        return text[0].upper() + text[1:] if text else ""

    @staticmethod
    def to_title_case(text):
        """Convert to title case"""
        return ' '.join(word.capitalize() for word in text.split())


class DataHelper:
    """Data transformation helper functions"""

    @staticmethod
    def dict_to_json(data):
        """Convert dictionary to JSON string"""
        return json.dumps(data, indent=2)

    @staticmethod
    def json_to_dict(json_str):
        """Convert JSON string to dictionary"""
        return json.loads(json_str)

    @staticmethod
    def filter_dict(data, keys):
        """Filter dictionary by keys"""
        return {k: v for k, v in data.items() if k in keys}

    @staticmethod
    def flatten_dict(data, parent_key='', sep='.'):
        """Flatten nested dictionary"""
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataHelper.flatten_dict(v, new_key, sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


class ConversionHelper:
    """Data type conversion helpers"""

    @staticmethod
    def to_int(value, default=0):
        """Safe conversion to integer"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_float(value, default=0.0):
        """Safe conversion to float"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def to_bool(value):
        """Convert value to boolean"""
        if isinstance(value, bool):
            return value
        return str(value).lower() in ['true', '1', 'yes', 'on']
