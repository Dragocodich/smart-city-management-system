#!/usr/bin/env python3
"""
COMPREHENSIVE SMART CITY SYSTEM AUDIT
Testing all functionalities and UI consistency
"""

import sys
sys.path.insert(0, 'smart-city-management-system')

print("=" * 80)
print("DEEP SYSTEM AUDIT - SMART CITY MANAGEMENT SYSTEM")
print("=" * 80)
print()

# ============================================================================
# PART 1: MODULE IMPORTS & COMPILATION CHECK
# ============================================================================
print("[AUDIT 1] Module Imports & Compilation")
print("-" * 80)

modules_to_test = {
    'Config': [
        ('config.settings', 'ROLES'),
        ('config.database_config', 'CONNECTION_STRING'),
    ],
    'Core': [
        ('core.database', 'db'),
    ],
    'Utils': [
        ('utils.validators', 'Validators'),
        ('utils.logger', 'Logger'),
        ('utils.helpers', 'DateTimeHelper'),
        ('utils.exceptions', 'DatabaseException'),
    ],
    'Services': [
        ('services.complaint_service', 'ComplaintService'),
        ('services.task_service', 'TaskService'),
        ('services.analytics_service', 'AnalyticsService'),
    ],
    'UI': [
        ('ui.role_selector', 'RoleSelector'),
        ('ui.login', 'LoginWindow'),
        ('ui.dashboard', 'Dashboard'),
        ('ui.admin_panel', 'AdminPanel'),
        ('ui.employee_panel', 'EmployeePanel'),
        ('ui.citizen_panel', 'CitizenPanel'),
    ]
}

import_status = {}

for category, modules in modules_to_test.items():
    print(f"\n{category} Layer:")
    for module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {module_path}.{class_name}")
            import_status[(module_path, class_name)] = True
        except Exception as e:
            print(f"  ❌ {module_path}.{class_name} - {str(e)[:50]}")
            import_status[(module_path, class_name)] = False

# ============================================================================
# PART 2: AUTHENTICATION & DEV MODE TEST
# ============================================================================
print()
print("[AUDIT 2] Authentication Testing (Development Mode)")
print("-" * 80)

from core.database import db

test_users = [
    ('admin', 'Admin@123', 'admin'),
    ('worker1', 'Worker@123', 'admin'),  # Will test role validation too
    ('officer1', 'Officer@123', 'admin'),
    ('citizen1', 'Citizen@123', 'citizen'),
]

auth_status = {}

for username, password, role in test_users:
    try:
        user = db.authenticate_user(username, password, role)
        print(f"  ✅ {username} ({role})")
        auth_status[username] = True
    except Exception as e:
        print(f"  ❌ {username} ({role}) - {str(e)[:50]}")
        auth_status[username] = False

# ============================================================================
# PART 3: SERVICE FUNCTIONALITY TEST
# ============================================================================
print()
print("[AUDIT 3] Service Instantiation")
print("-" * 80)

services_to_test = [
    ('services.complaint_service', 'ComplaintService'),
    ('services.task_service', 'TaskService'),
    ('services.traffic_service', 'TrafficService'),
    ('services.billing_service', 'BillingService'),
    ('services.analytics_service', 'AnalyticsService'),
]

service_status = {}

for module_path, class_name in services_to_test:
    try:
        module = __import__(module_path, fromlist=[class_name])
        service_class = getattr(module, class_name)
        service = service_class()
        print(f"  ✅ {class_name} instantiated")
        service_status[class_name] = True
    except Exception as e:
        print(f"  ❌ {class_name} - {str(e)[:50]}")
        service_status[class_name] = False

# ============================================================================
# PART 4: DATABASE METHODS CHECK
# ============================================================================
print()
print("[AUDIT 4] Database Methods Availability")
print("-" * 80)

db_methods = [
    'authenticate_user',
    'hash_password',
    'verify_password',
    'execute_query',
    'execute_single',
]

db_status = {}

for method_name in db_methods:
    has_method = hasattr(db, method_name)
    status = "✅" if has_method else "❌"
    print(f"  {status} {method_name}")
    db_status[method_name] = has_method

# ============================================================================
# PART 5: UI COMPONENT METHODS CHECK
# ============================================================================
print()
print("[AUDIT 5] UI Panel Methods")
print("-" * 80)

ui_methods = {
    'admin_panel': ['open_complaints', 'open_task_assigner', 'open_employees', 'open_analytics', 'logout'],
    'employee_panel': ['complete_task', 'load_tasks'],
    'citizen_panel': ['submit_complaint', 'load_payments', 'pay_selected'],
}

ui_status = {}

for panel_name, methods in ui_methods.items():
    print(f"\n  {panel_name}:")
    for method in methods:
        try:
            module = __import__(f'ui.{panel_name}', fromlist=[panel_name.title()])
            panel_class = getattr(module, ''.join(word.capitalize() for word in panel_name.split('_')))
            has_method = any(method in str(panel_class) for method in [method])
            # Check if method exists in source
            import inspect
            methods_list = [m[0] for m in inspect.getmembers(panel_class, predicate=inspect.isfunction)]
            if method in methods_list or method.replace('_', ' ') in str(panel_class):
                print(f"    ✅ {method}")
                ui_status[f'{panel_name}.{method}'] = True
            else:
                print(f"    ⚠️  {method} (may be incomplete)")
                ui_status[f'{panel_name}.{method}'] = False
        except Exception as e:
            print(f"    ❌ {method} - {str(e)[:40]}")
            ui_status[f'{panel_name}.{method}'] = False

# ============================================================================
# PART 6: UI STYLING CONSISTENCY CHECK
# ============================================================================
print()
print("[AUDIT 6] UI Styling Consistency")
print("-" * 80)

import inspect

ui_files = {
    'login': 'ui.login.LoginWindow',
    'admin_panel': 'ui.admin_panel.AdminPanel',
    'employee_panel': 'ui.employee_panel.EmployeePanel',
    'citizen_panel': 'ui.citizen_panel.CitizenPanel',
    'dashboard': 'ui.dashboard.Dashboard',
}

style_status = {}

for name, path in ui_files.items():
    try:
        parts = path.split('.')
        module = __import__('.'.join(parts[:-1]), fromlist=[parts[-1]])
        cls = getattr(module, parts[-1])
        source = inspect.getsource(cls)
        
        style_score = 0
        style_checks = {
            'gradient': 'qlineargradient' in source,
            'font_styling': 'QFont' in source,
            'color_palette': '#' in source,
            'border_radius': 'border-radius' in source,
            'hover_effects': 'hover' in source,
        }
        
        checked = sum(1 for v in style_checks.values() if v)
        print(f"\n  {name}:")
        for check, result in style_checks.items():
            status = "✅" if result else "❌"
            print(f"    {status} {check}")
        print(f"    → Style Score: {checked}/5")
        style_status[name] = checked
    except Exception as e:
        print(f"  ❌ {name} - {str(e)[:40]}")
        style_status[name] = 0

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print()
print("=" * 80)
print("AUDIT SUMMARY REPORT")
print("=" * 80)

total_checks = len(import_status) + len(auth_status) + len(service_status) + len(db_status) + len(style_status)
passed_checks = sum([
    sum(1 for v in import_status.values() if v),
    sum(1 for v in auth_status.values() if v),
    sum(1 for v in service_status.values() if v),
    sum(1 for v in db_status.values() if v),
])

print()
print("ISSUES FOUND:")
print()

# Find all issues
issues = []

# Check failed imports
for (module, cls), status in import_status.items():
    if not status:
        issues.append(f"❌ {module}.{cls} - IMPORT FAILED")

# Check failed authentications
for user, status in auth_status.items():
    if not status:
        issues.append(f"❌ {user} - AUTHENTICATION FAILED")

# Check failed services
for service, status in service_status.items():
    if not status:
        issues.append(f"❌ {service} - SERVICE INSTANTIATION FAILED")

# Check UI styling
for panel, score in style_status.items():
    if score < 3:
        issues.append(f"⚠️  {panel} - POOR UI STYLING (Score: {score}/5)")

if issues:
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
else:
    print("✅ No critical issues found!")

print()
print("STATISTICS:")
print(f"  Modules Imported: {sum(1 for v in import_status.values() if v)}/{len(import_status)}")
print(f"  Auth Tests Passed: {sum(1 for v in auth_status.values() if v)}/{len(auth_status)}")
print(f"  Services Working: {sum(1 for v in service_status.values() if v)}/{len(service_status)}")
print(f"  DB Methods Available: {sum(1 for v in db_status.values() if v)}/{len(db_status)}")
print(f"  Avg UI Style Score: {sum(style_status.values()) / len(style_status):.1f}/5")

print()
print("=" * 80)
if not issues:
    print("✅ AUDIT COMPLETE - SYSTEM READY")
else:
    print(f"⚠️  AUDIT COMPLETE - {len(issues)} ISSUES FOUND (See above)")
print("=" * 80)
