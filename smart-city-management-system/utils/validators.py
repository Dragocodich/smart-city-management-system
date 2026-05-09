# ============================================================
# DATA VALIDATORS
# ============================================================

import re
from datetime import datetime

class Validators:
    """Data validation utility class"""

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        pattern = r'^[\d\s\-\+\(\)]{10,}$'
        return re.match(pattern, str(phone)) is not None

    @staticmethod
    def validate_username(username):
        """Validate username (3-50 characters, alphanumeric + underscore)"""
        if len(username) < 3 or len(username) > 50:
            return False
        pattern = r'^[a-zA-Z0-9_]+$'
        return re.match(pattern, username) is not None

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain a digit"
        return True, "Password is strong"

    @staticmethod
    def validate_cnic(cnic):
        """Validate CNIC format (Pakistani ID)"""
        cnic = cnic.replace("-", "").replace(" ", "")
        return len(cnic) == 13 and cnic.isdigit()

    @staticmethod
    def validate_date(date_str, date_format="%Y-%m-%d"):
        """Validate date format"""
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_numeric(value, min_val=None, max_val=None):
        """Validate numeric value within range"""
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_empty(value):
        """Check if value is empty or None"""
        if value is None:
            return False
        if isinstance(value, str) and value.strip() == "":
            return False
        return True
