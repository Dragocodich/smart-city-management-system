#!/usr/bin/env python3
"""Test all module imports for Smart City Management System"""

import sys
sys.path.insert(0, 'smart-city-management-system')

print("=" * 60)
print("SMART CITY MANAGEMENT SYSTEM - IMPORT TEST")
print("=" * 60)
print()

passed = 0
failed = 0

# 1. CONFIG LAYER
print("[1] CONFIG LAYER")
try:
    from config.settings import ROLES
    print("    [OK] settings - Loaded successfully")
    print(f"        -> Available roles: {len(ROLES)}")
    passed += 1
except Exception as e:
    print(f"    [FAIL] settings - {e}")
    failed += 1

try:
    from config.database_config import CONNECTION_STRING
    print("    [OK] database_config - Loaded successfully")
    passed += 1
except Exception as e:
    print(f"    [FAIL] database_config - {e}")
    failed += 1

# 2. CORE LAYER
print()
print("[2] CORE LAYER")
try:
    from core.database import db
    print("    [OK] database - DatabaseManager loaded")
    print(f"        -> Connection status: {'Active' if db.conn else 'None (expected in dev mode)'}")
    passed += 1
except Exception as e:
    print(f"    [FAIL] database - {e}")
    failed += 1

# 3. UTILS LAYER
print()
print("[3] UTILS LAYER")
try:
    from utils.validators import Validators
    print("    [OK] validators - Loaded successfully")
    passed += 1
except Exception as e:
    print(f"    [FAIL] validators - {e}")
    failed += 1

try:
    from utils.logger import Logger
    print("    [OK] logger - Loaded successfully")
    passed += 1
except Exception as e:
    print(f"    [FAIL] logger - {e}")
    failed += 1

try:
    from utils.helpers import DateTimeHelper, StringHelper
    print("    [OK] helpers - Loaded successfully")
    passed += 1
except Exception as e:
    print(f"    [FAIL] helpers - {e}")
    failed += 1

try:
    from utils.exceptions import DatabaseException
    print("    [OK] exceptions - Loaded successfully")
    passed += 1
except Exception as e:
    print(f"    [FAIL] exceptions - {e}")
    failed += 1

# 4. DATA LAYER
print()
print("[4] DATA LAYER (Repositories)")
try:
    from data.repositories import (
        ComplaintRepository, TaskRepository, EmployeeRepository,
        CitizenRepository, VehicleRepository, DepartmentRepository,
        UtilityRepository, PaymentRepository
    )
    print("    [OK] repositories - 8+ repositories loaded")
    passed += 1
except Exception as e:
    print(f"    [FAIL] repositories - {e}")
    failed += 1

# 5. SERVICES LAYER
print()
print("[5] SERVICES LAYER")
services = [
    ("complaint_service", "ComplaintService"),
    ("task_service", "TaskService"),
    ("traffic_service", "TrafficService"),
    ("billing_service", "BillingService"),
    ("analytics_service", "AnalyticsService"),
    ("incident_service", "IncidentService"),
    ("waste_service", "WasteService"),
    ("utility_service", "UtilityService"),
]

for module, classname in services:
    try:
        exec(f"from services.{module} import {classname}")
        print(f"    [OK] {module}")
        passed += 1
    except Exception as e:
        print(f"    [FAIL] {module} - {e}")
        failed += 1

# 6. UI LAYER
print()
print("[6] UI LAYER")
try:
    from ui.login import LoginWindow
    print("    [OK] login - LoginWindow loaded")
    passed += 1
except Exception as e:
    print(f"    [FAIL] login - {e}")
    failed += 1

try:
    from ui.admin_panel import AdminPanel
    print("    [OK] admin_panel - AdminPanel loaded [FIXED]")
    passed += 1
except Exception as e:
    print(f"    [FAIL] admin_panel - {e}")
    failed += 1

try:
    from ui.role_selector import RoleSelector
    print("    [OK] role_selector - RoleSelector loaded")
    passed += 1
except Exception as e:
    print(f"    [FAIL] role_selector - {e}")
    failed += 1

try:
    from ui.dashboard import Dashboard
    print("    [OK] dashboard - Dashboard loaded")
    passed += 1
except Exception as e:
    print(f"    [FAIL] dashboard - {e}")
    failed += 1

# SUMMARY
print()
print("=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed")
print("=" * 60)

if failed == 0:
    print("[SUCCESS] All modules import successfully!")
    sys.exit(0)
else:
    print("[ERROR] Some modules failed to import")
    sys.exit(1)
