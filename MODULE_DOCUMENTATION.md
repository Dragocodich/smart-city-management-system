# ============================================================
# SMART CITY MANAGEMENT SYSTEM - REFACTORED PROJECT STRUCTURE
# ============================================================

## PROJECT OVERVIEW

This document outlines the complete refactored structure of the Smart City Management System ERP, 
organized for scalability, maintainability, and efficient development.

## DIRECTORY STRUCTURE

```
smart-city-management-system/
├── config/                          # Configuration & Settings
│   ├── __init__.py
│   ├── database_config.py           # Database connection settings
│   └── settings.py                  # Application settings & constants
│
├── core/                             # Core Framework
│   ├── __init__.py
│   └── database.py                  # Refactored database manager (Singleton)
│
├── data/                             # Data Access Layer
│   ├── repositories.py              # Repository pattern implementations
│   └── __init__.py
│
├── services/                         # Business Logic Layer
│   ├── complaint_service.py          # Complaint management logic
│   ├── traffic_service.py            # Traffic management logic
│   ├── waste_service.py              # Waste management logic
│   ├── utility_service.py            # Utility monitoring logic
│   ├── billing_service.py            # Billing & payment logic
│   ├── incident_service.py           # Emergency & incidents logic
│   ├── task_service.py               # Task management logic
│   ├── user_service.py               # User account management
│   ├── analytics_service.py          # Analytics & reporting logic
│   └── __init__.py
│
├── utils/                            # Utility Functions
│   ├── validators.py                # Data validation helpers
│   ├── logger.py                    # Centralized logging system
│   ├── helpers.py                   # General helper functions
│   ├── exceptions.py                # Custom exception classes
│   └── __init__.py
│
├── ui/                               # User Interface (PyQt6)
│   ├── role_selector.py             # Role selection screen
│   ├── login.py                     # Login authentication UI
│   ├── dashboard.py                 # Main dashboard router
│   ├── admin_panel.py               # Admin dashboard
│   ├── employee_panel.py            # Employee dashboard
│   ├── citizen_panel.py             # Citizen portal
│   ├── styles/                      # UI stylesheets
│   │   ├── main_style.css
│   │   └── theme.css
│   ├── windows/                     # Sub-windows & dialogs
│   │   ├── complaint_window.py
│   │   ├── task_window.py
│   │   ├── traffic_window.py
│   │   ├── waste_window.py
│   │   ├── billing_window.py
│   │   ├── incident_window.py
│   │   ├── employee_window.py
│   │   └── analytics_window.py
│   └── __pycache__/
│
├── logs/                             # Application logs
│   └── app_YYYYMMDD.log
│
├── database/                         # Database files
│   └── smartcity.sql                # Complete SQL schema
│
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies
├── setup.sh                          # Linux/Mac setup script
├── install_requirements.py           # Windows setup script
├── README.md                         # Project documentation
└── SETUP_GUIDE.md                   # Setup instructions
```

---

## CORE MODULES (IMPLEMENTED)

### Configuration Module (`config/`)

#### `database_config.py`
- **Purpose**: Database connection configuration
- **Key Variables**:
  - `DB_CONFIG`: Database connection parameters
  - `CONNECTION_STRING`: ODBC connection string
  - `QUERY_TIMEOUTS`: Query timeout settings

#### `settings.py`
- **Purpose**: Application settings and constants
- **Exports**:
  - `WINDOW_WIDTH`, `WINDOW_HEIGHT`: UI dimensions
  - `THEME`: Color scheme definitions
  - `ROLES`: User role definitions
  - `PRIORITIES`: Task/complaint priority levels
  - `COMPLAINT_STATUS`: Complaint status values
  - `TASK_STATUS`: Task status values
  - `DEPARTMENTS`: Department list

---

### Core Database Module (`core/`)

#### `database.py` - DatabaseManager (Singleton Pattern)
- **Class**: `DatabaseManager`
- **Key Methods**:
  - `connect()`: Establish database connection
  - `disconnect()`: Close database connection
  - `execute_query()`: Execute SELECT queries (multiple rows)
  - `execute_single()`: Execute SELECT queries (single row)
  - `execute_update()`: Execute INSERT/UPDATE/DELETE
  - `execute_batch()`: Execute batch operations
  - `hash_password()`: Hash passwords with bcrypt
  - `verify_password()`: Verify password hashes
  - `authenticate_user()`: User authentication
  - `begin_transaction()`, `commit_transaction()`, `rollback_transaction()`: Transaction management

---

### Data Access Layer (`data/`)

#### `repositories.py` - Repository Pattern Implementation

**BaseRepository**
- Generic CRUD operations for any table
- `get_by_id()`, `get_all()`, `get_by_filter()`, `count()`

**CitizenRepository**
- Extends BaseRepository for citizens table
- `get_by_username()`, `get_active_citizens()`, `create_citizen()`

**EmployeeRepository**
- Extends BaseRepository for employees table
- `get_by_username()`, `get_by_department()`, `get_active_employees()`

**DepartmentRepository**
- Extends BaseRepository for departments table
- `get_by_name()`

**ComplaintRepository**
- Extends BaseRepository for complaints table
- `get_by_citizen()`, `get_by_status()`, `get_pending_complaints()`

**TaskRepository**
- Extends BaseRepository for tasks table
- `get_by_employee()`, `get_by_status()`, `get_pending_tasks()`

**VehicleRepository**
- Extends BaseRepository for vehicles table
- `get_available_vehicles()`, `get_by_department()`

**UtilityRepository**
- Extends BaseRepository for utilities table
- `get_by_citizen()`, `get_by_type()`

**PaymentRepository**
- Extends BaseRepository for payments table
- `get_by_citizen()`, `get_pending_payments()`, `get_overdue_payments()`

---

## BUSINESS LOGIC LAYER - SERVICES (`services/`)

### 1. ComplaintService (`complaint_service.py`)
**Purpose**: Manage citizen complaints and resolution

**Key Methods**:
- `submit_complaint()`: Create new complaint
- `get_complaint_details()`: Retrieve complaint info
- `update_status()`: Update complaint status
- `assign_task()`: Create task from complaint
- `get_pending_complaints()`: Get unresolved complaints
- `get_citizen_complaints()`: Get citizen's complaints
- `rate_complaint()`: Add citizen satisfaction rating
- `get_statistics()`: Complaint system statistics

---

### 2. TrafficService (`traffic_service.py`)
**Purpose**: Manage smart traffic system

**Key Methods**:
- `record_traffic_data()`: Log sensor traffic data
- `get_congestion_level()`: Current zone congestion
- `analyze_traffic_pattern()`: Historical traffic analysis
- `adjust_signal_timing()`: Auto-adjust traffic signals
- `get_all_sensors()`: Retrieve all sensors
- `get_sensors_by_zone()`: Filter sensors by location
- `register_sensor()`: Add new traffic sensor
- `get_traffic_alerts()`: Critical congestion alerts
- `get_traffic_statistics()`: System-wide metrics

---

### 3. WasteService (`waste_service.py`)
**Purpose**: Manage waste collection operations

**Key Methods**:
- `schedule_collection()`: Schedule waste pickup
- `start_collection()`: Begin collection route
- `complete_collection()`: Mark collection done
- `get_scheduled_collections()`: View scheduled routes
- `optimize_route()`: Suggest efficient collection route
- `get_available_vehicles()`: View available trucks
- `register_vehicle()`: Add new waste vehicle
- `get_waste_statistics()`: Collection metrics

---

### 4. UtilityService (`utility_service.py`)
**Purpose**: Monitor utility consumption

**Key Methods**:
- `record_meter_reading()`: Log meter readings
- `get_citizen_utilities()`: Get citizen's utilities
- `get_utility_readings()`: Consumption history
- `monitor_consumption()`: Track utility usage
- `get_zone_consumption()`: Area-wide consumption
- `get_high_consumers()`: Identify heavy users
- `get_utility_statistics()`: System statistics

---

### 5. BillingService (`billing_service.py`)
**Purpose**: Handle utility billing and payments

**Key Methods**:
- `generate_bill()`: Create utility bill
- `process_payment()`: Record payment
- `get_pending_bills()`: View unpaid bills
- `get_payment_history()`: Payment records
- `check_overdue_payments()`: Mark overdue
- `get_bill_statistics()`: Billing metrics
- `generate_bill_to_citizen()`: Auto-generate monthly bills
- `send_payment_reminder()`: Due payment alerts

---

### 6. IncidentService (`incident_service.py`)
**Purpose**: Handle emergency incidents and alerts

**Key Methods**:
- `report_incident()`: Create incident report
- `get_open_incidents()`: View active incidents
- `get_incident_by_severity()`: Filter by severity
- `update_incident_status()`: Update incident status
- `resolve_incident()`: Mark incident resolved
- `create_alert()`: Generate system alert
- `get_active_alerts()`: View active alerts
- `get_alerts_by_role()`: Role-specific alerts
- `mark_alert_read()`: Mark alert as acknowledged
- `get_incident_statistics()`: System metrics
- `get_incident_response_time()`: Response duration analysis

---

### 7. TaskService (`task_service.py`)
**Purpose**: Manage work task assignments

**Key Methods**:
- `create_task()`: Create new task
- `get_employee_tasks()`: Get employee's assigned tasks
- `get_pending_tasks()`: View incomplete tasks
- `update_task_status()`: Update task progress
- `start_task()`: Mark task in progress
- `complete_task()`: Mark task done
- `reassign_task()`: Reassign to different employee
- `extend_due_date()`: Extend deadline
- `get_overdue_tasks()`: Overdue task notifications
- `get_task_statistics()`: Task metrics
- `get_employee_performance()`: Employee productivity metrics

---

### 8. UserManagementService (`user_service.py`)
**Purpose**: Handle user account management

**Key Methods**:
- `create_employee()`: Create employee account
- `create_citizen()`: Register citizen
- `update_employee_profile()`: Update employee info
- `update_citizen_profile()`: Update citizen info
- `change_password()`: Password change
- `deactivate_user()`: Disable account
- `activate_user()`: Enable account
- `record_login()`: Log login activity

---

### 9. AnalyticsService (`analytics_service.py`)
**Purpose**: Generate system-wide analytics and reports

**Key Methods**:
- `get_dashboard_summary()`: Overall system summary
- `get_performance_report()`: Period performance report
- `get_department_performance()`: Department metrics
- `_get_complaint_summary()`: Complaint statistics
- `_get_task_summary()`: Task completion stats
- `_get_traffic_summary()`: Traffic system stats
- `_get_waste_summary()`: Waste collection stats
- `_get_billing_summary()`: Revenue & billing stats
- `_get_incident_summary()`: Emergency incident stats

---

## UTILITY MODULES (`utils/`)

### `validators.py` - Input Validation
**Class**: `Validators` (Static Methods)
- `validate_email()`: Email format
- `validate_phone()`: Phone number format
- `validate_username()`: Username requirements
- `validate_password()`: Password strength
- `validate_cnic()`: CNIC format (Pakistan)
- `validate_date()`: Date format
- `validate_numeric()`: Numeric range
- `validate_empty()`: Null/empty check

### `logger.py` - Centralized Logging
**Class**: `Logger` (Singleton Pattern)
- `info()`: Info level logging
- `warning()`: Warning level logging
- `error()`: Error level logging
- `debug()`: Debug level logging
- `critical()`: Critical level logging

### `helpers.py` - Helper Functions

**DateTimeHelper**
- `now()`: Current datetime
- `today()`: Current date
- `add_days()`: Add days to current date
- `get_month_start()`: First day of month
- `get_month_end()`: Last day of month

**StringHelper**
- `truncate()`: Truncate string
- `capitalize_first()`: Capitalize first letter
- `to_title_case()`: Convert to title case

**DataHelper**
- `dict_to_json()`: Dictionary to JSON
- `json_to_dict()`: JSON to dictionary
- `filter_dict()`: Filter dictionary keys
- `flatten_dict()`: Flatten nested dictionary

**ConversionHelper**
- `to_int()`: Safe integer conversion
- `to_float()`: Safe float conversion
- `to_bool()`: Value to boolean conversion

### `exceptions.py` - Custom Exceptions
- `SmartCityException`: Base exception
- `DatabaseException`: Database errors
- `AuthenticationException`: Auth failures
- `AuthorizationException`: Permission errors
- `ValidationException`: Data validation errors
- `ResourceNotFoundException`: Resource not found
- `DuplicateResourceException`: Duplicate data
- `ConfigurationException`: Config errors
- `NotImplementedException`: Not yet implemented

---

## USER INTERFACE MODULES (`ui/`)

### Existing Modules (Partially Complete)
- `role_selector.py`: Role selection screen
- `login.py`: User authentication
- `dashboard.py`: Main dashboard router
- `admin_panel.py`: Admin interface
- `employee_panel.py`: Employee interface
- `citizen_panel.py`: Citizen portal

### Required New UI Windows (`ui/windows/`)

#### Management Windows
- **`complaint_window.py`**: Complaint submission & tracking
- **`task_window.py`**: Task assignment & tracking
- **`employee_window.py`**: Employee management
- **`department_window.py`**: Department management

#### Operations Windows
- **`traffic_window.py`**: Traffic monitoring & control
- **`waste_window.py`**: Waste collection management
- **`utility_window.py`**: Utility monitoring dashboard
- **`billing_window.py`**: Billing & payment interface
- **`incident_window.py`**: Emergency incident management
- **`analytics_window.py`**: Reports & analytics dashboard

#### Additional Windows
- **`profile_window.py`**: User profile management
- **`alert_window.py`**: System alerts display
- **`settings_window.py`**: Application settings

### UI Styling (`ui/styles/`)
- **`main_style.css`**: Global stylesheet
- **`theme.css`**: Theme definitions

---

## ENTRY POINT

### `main.py`
```python
- Initialize application (QApplication)
- Connect to database
- Show role selector window
- Execute application event loop
```

---

## DEPENDENCIES

### `requirements.txt`
```
PyQt6==6.7.0            # GUI Framework
pyodbc==5.0.1           # SQL Server connection
bcrypt==4.1.1           # Password hashing
python-dotenv==1.0.0    # Environment variables
reportlab==4.0.0        # PDF generation (future)
pandas==2.0.0           # Data analysis (future)
openpyxl==3.1.0         # Excel export (future)
```

---

## MODULE DEPENDENCIES MAP

```
main.py
└── ui.role_selector
    └── ui.login
        └── core.database
            ├── config.database_config
            └── config.settings
        └── ui.dashboard
            ├── ui.admin_panel
            ├── ui.employee_panel
            └── ui.citizen_panel

Services Layer
├── services.complaint_service
├── services.traffic_service
├── services.waste_service
├── services.utility_service
├── services.billing_service
├── services.incident_service
├── services.task_service
├── services.user_service
└── services.analytics_service

Data Layer
└── data.repositories
    └── core.database

Utilities
├── utils.validators
├── utils.logger
├── utils.helpers
└── utils.exceptions
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Core Infrastructure (COMPLETED)
- [x] Database manager refactoring
- [x] Configuration module
- [x] Repository pattern
- [x] Exception handling
- [x] Utilities module

### Phase 2: Service Layer (COMPLETED)
- [x] ComplaintService
- [x] TrafficService
- [x] WasteService
- [x] UtilityService
- [x] BillingService
- [x] IncidentService
- [x] TaskService
- [x] UserManagementService
- [x] AnalyticsService

### Phase 3: UI Implementation (IN PROGRESS)
- [ ] Complete existing panels
- [ ] Create management windows
- [ ] Create operations windows
- [ ] Implement styling

### Phase 4: Advanced Features (PENDING)
- [ ] Report generation (PDF/Excel)
- [ ] Email notifications
- [ ] SMS alerts
- [ ] Data export
- [ ] Advanced analytics
- [ ] Real-time dashboards

### Phase 5: Security & Testing (PENDING)
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] Role-based access control
- [ ] Audit logging
- [ ] Unit tests
- [ ] Integration tests

---

## USAGE EXAMPLES

### Using Services
```python
from services.complaint_service import ComplaintService
from services.traffic_service import TrafficService

complaint_svc = ComplaintService()
complaint_svc.submit_complaint(
    citizen_id=1,
    dept_id=2,
    title="Pothole on Main Street",
    description="Large pothole near intersection",
    category="Road Maintenance",
    location="Main St & 5th Ave"
)

traffic_svc = TrafficService()
traffic_svc.record_traffic_data(
    sensor_id=1,
    intersection="Main & 5th",
    zone="Zone A",
    vehicle_count=150,
    congestion_level="High"
)
```

### Database Operations
```python
from core.database import db
from data.repositories import ComplaintRepository

db.connect()
complaint_repo = ComplaintRepository()
pending = complaint_repo.get_pending_complaints()
```

### Validation
```python
from utils.validators import Validators

if Validators.validate_email(email):
    # Process email
    pass

password_valid, msg = Validators.validate_password(pwd)
```

---

## DEPLOYMENT NOTES

1. **Database Setup**: Execute `database/smartcity.sql` on MS SQL Server
2. **Environment**: Configure `config/database_config.py`
3. **Dependencies**: Run `pip install -r requirements.txt`
4. **Logs**: Check `logs/` directory for application logs
5. **Run**: Execute `python main.py`

---

## FUTURE ENHANCEMENTS

1. Web-based dashboard
2. Mobile application
3. Real-time notifications
4. Advanced GIS mapping
5. Machine learning predictions
6. IoT integration
7. Blockchain for payment tracking
8. Multi-language support
9. API layer for third-party integration
10. Cloud deployment options
