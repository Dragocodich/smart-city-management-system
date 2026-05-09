# ============================================================
# APPLICATION SETTINGS
# ============================================================

# UI Settings
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Themes
THEME = {
    "primary_color": "#3498db",
    "secondary_color": "#2c3e50",
    "success_color": "#27ae60",
    "warning_color": "#f39c12",
    "danger_color": "#e74c3c",
    "info_color": "#16a085",
}

# Roles
ROLES = {
    "admin": "City Admin",
    "officer": "Department Officer",
    "worker": "Field Worker",
    "emergency": "Emergency Services",
    "citizen": "Citizen",
}

# Priorities
PRIORITIES = ["Low", "Normal", "High", "Critical"]

# Status Values
COMPLAINT_STATUS = ["Submitted", "Assigned", "In Progress", "Resolved", "Closed"]
TASK_STATUS = ["Pending", "In Progress", "Completed", "Cancelled"]
WASTE_STATUS = ["Scheduled", "In Progress", "Completed", "Cancelled"]

# Departments
DEPARTMENTS = [
    "Traffic Management",
    "Waste Management",
    "Utilities",
    "Public Safety",
    "Transportation",
    "Emergency Services",
    "Infrastructure",
]

# Pagination
ITEMS_PER_PAGE = 10

# Report Settings
REPORT_FORMAT = ["PDF", "Excel", "CSV"]
