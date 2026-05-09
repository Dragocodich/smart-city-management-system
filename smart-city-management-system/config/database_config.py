# ============================================================
# DATABASE CONFIGURATION
# ============================================================

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# SQL Server Connection Configuration
DB_CONFIG = {
    "driver": os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}"),
    "server": os.getenv("DB_SERVER", "DESKTOP-62TRPPU\\SQLEXPRESS"),
    "database": os.getenv("DB_NAME", "SmartCityDB"),
    "trusted_connection": os.getenv("DB_TRUSTED", "yes"),
}

# Connection String
CONNECTION_STRING = (
    f"DRIVER={DB_CONFIG['driver']};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
)

# Query Types
QUERY_TIMEOUTS = {
    "default": 30,
    "analytics": 60,
    "reporting": 120,
}
