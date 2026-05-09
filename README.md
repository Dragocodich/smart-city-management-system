# 🏙️ Smart City Management System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.7.0-green)
![SQL Server](https://img.shields.io/badge/SQL%20Server-ODBC-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive desktop application for managing smart city operations with multi-role access control, complaint management, task assignment, and utility billing systems.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [User Roles & Capabilities](#user-roles--capabilities)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [Development Guide](#development-guide)

---

## 🎯 Project Overview

The **Smart City Management System** is a Python-based desktop application designed to streamline city operations and services. It provides a centralized platform for:

- **Citizens**: Submit complaints, view bills, and pay utilities
- **Employees**: Manage assigned tasks and track progress
- **Admins**: Oversee all operations, manage complaints, assign tasks, and view analytics

### Real-World Use Cases
- 🚨 **Complaint Management**: Citizens report issues (potholes, broken lights, water leaks), employees resolve them
- 👨‍💼 **Task Management**: Admins assign tasks to employees with tracking and deadlines
- 💰 **Utility Billing**: Track electricity, water, and gas consumption with payment status
- 🚗 **Traffic Management**: Monitor real-time congestion levels via sensors
- 🗑️ **Waste Collection**: Schedule and track waste collection routes by zone
- 👥 **Department Management**: Organize employees by departments with role-based access

---

## ✨ Key Features

### For Citizens
- ✅ User registration and secure login
- ✅ Submit service complaints with categories and priority levels
- ✅ Track complaint status in real-time
- ✅ View utility bills (electricity, water, gas)
- ✅ Pay bills online with transaction tracking
- ✅ Rate service quality (1-5 stars) after complaint resolution

### For Employees
- ✅ Role-based access (officer, worker, emergency responder)
- ✅ View assigned tasks from admin with full details
- ✅ Update task status (Pending → In Progress → Completed)
- ✅ Mark tasks as complete with automatic timestamps
- ✅ Belong to specific departments

### For Admins
- ✅ Full system access and control
- ✅ View and manage all complaints with filtering
- ✅ Assign tasks to employees with priority and deadlines
- ✅ Manage employee accounts and departments
- ✅ View system analytics and statistics
- ✅ Monitor active users and audit logs

### System-Wide Features
- 🔐 **Secure Authentication**: Bcrypt password hashing
- 🔑 **Role-Based Authorization**: Different features for different user types
- 📊 **Real-time Updates**: Live task and complaint status updates
- 🔄 **Database Transactions**: Safe data operations with error handling
- 📱 **Responsive UI**: PyQt6-based modern graphical interface

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend** | PyQt6 | 6.7.0 | Desktop GUI framework |
| **Backend** | Python | 3.8+ | Application logic |
| **Database** | MS SQL Server | 2017+ | Data persistence |
| **Driver** | pyodbc | 5.0.1 | Database connectivity |
| **Security** | bcrypt | 4.1.1 | Password hashing |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│           PRESENTATION LAYER (PyQt6 GUI)               │
├─────────────────────────────────────────────────────────┤
│ RoleSelector → LoginWindow → Dashboard → Role Panels   │
│ (Select role)  (Authenticate)  (Router)   (Features)   │
├─────────────────────────────────────────────────────────┤
│          BUSINESS LOGIC LAYER (db.py)                  │
├─────────────────────────────────────────────────────────┤
│ Authentication │ Complaints │ Tasks │ Billing │ More   │
├─────────────────────────────────────────────────────────┤
│        DATA ACCESS LAYER (pyodbc + SQL Server)          │
├─────────────────────────────────────────────────────────┤
│              MS SQL Server Database                     │
│  Employees │ Citizens │ Complaints │ Tasks │ Utilities  │
│  Depts │ Services │ Payments │ Traffic │ Waste         │
└─────────────────────────────────────────────────────────┘
```

### Application Entry Flow

```
START
  ↓
main.py (Initialize PyQt6 app)
  ↓
db.connect() (Connect to SQL Server)
  ↓
RoleSelector Window (Choose: Admin/Employee/Citizen)
  ↓
LoginWindow (Enter credentials)
  ↓
db.authenticate_user() (Verify with bcrypt)
  ↓
Dashboard Router (Route based on role)
  ├→ AdminPanel (Complaints, Tasks, Employees, Analytics)
  ├→ EmployeePanel (View Assigned Tasks, Update Status)
  └→ CitizenPanel (Submit Complaints, View Bills, Pay)
  ↓
User Interactions & Database Updates
  ↓
Logout → Return to RoleSelector
```

---

## 📊 Database Schema Overview

### Main Tables

**Departments** - Organizational units (Police, Fire, Health, etc.)
- dept_id, dept_name, dept_code, head_name, email, phone

**Employees** - City staff members
- emp_id, dept_id, username, password_hash (bcrypt), full_name
- role: 'admin' | 'officer' | 'worker' | 'emergency'
- email, phone, hire_date, is_active, last_login

**Citizens** - Registered residents
- citizen_id, username, password_hash, full_name, cnic, email
- phone, address, zone, registered_at, is_active

**Complaints** - Service complaints/requests
- complaint_id, citizen_id, dept_id, title, description
- category, priority ('Low'|'Normal'|'High'|'Critical')
- status ('Submitted'|'Assigned'|'In Progress'|'Resolved'|'Closed')
- location, submitted_at, resolved_at, citizen_rating (1-5 stars)

**Tasks** - Work assignments (linked to complaints)
- task_id, complaint_id, assigned_to (employee), assigned_by (admin)
- title, description, priority, status, due_date, created_at, completed_at

**Utilities** - Meter readings (Electricity, Water, Gas)
- utility_id, citizen_id, utility_type, meter_no
- prev_reading, curr_reading, units_consumed, rate_per_unit
- reading_date, zone

**Payments** - Billing and transactions
- payment_id, citizen_id, utility_id, amount, total_amount
- status ('Pending'|'Paid'|'Overdue'|'Cancelled')
- due_date, paid_at, bill_month, transaction_ref

**Traffic Data** - Real-time sensor data
- data_id, sensor_id, intersection, zone, vehicle_count
- congestion_level ('Low'|'Moderate'|'High'|'Critical')
- signal_timing_ns, signal_timing_ew, recorded_at

**Waste Collection** - Garbage collection tracking
- collection_id, vehicle_id, zone, route_info, bins_collected, weight_kg
- status ('Scheduled'|'In Progress'|'Completed'|'Cancelled')
- scheduled_at, completed_at

**Services** - City services offered by departments
- service_id, dept_id, service_name, description, is_active

---

## 👥 User Roles & Capabilities

### Admin (System Administrator)
| Feature | What It Does |
|---------|-------------|
| 👁️ Dashboard | View system overview, statistics |
| 📋 Manage Complaints | View all complaints, filter by status/priority |
| 👨‍💼 Assign Tasks | Create tasks, assign to employees, set deadlines |
| 👥 Manage Employees | Add/edit/deactivate employee accounts |
| 📊 Analytics | View complaint resolution rates, system performance |

**Example Admin Workflow:**
```
1. Login as Admin
2. See Dashboard: 150 total complaints, 23 unresolved
3. View complaint: "Pothole on Main Street" from Alice
4. Create task: Assign to John (Road Maintenance)
5. Set priority: High, Due date: Tomorrow
6. Monitor task status: Pending → In Progress → Completed
7. Close complaint and rate: Resolved
```

---

### Employee (Officer/Worker/Emergency)
| Feature | What It Does |
|---------|-------------|
| 👁️ View Tasks | See all tasks assigned by admin |
| ✏️ Update Status | Mark task progress: Pending → In Progress → Completed |
| 📝 Add Notes | Add comments or notes to tasks |
| 📊 My Performance | View completed tasks and statistics |

**Example Employee Workflow:**
```
1. Login as Employee (John - Maintenance Worker)
2. View 5 assigned tasks
3. Click Task: "Fix pothole on Main Street"
4. Change status: Pending → In Progress
5. Go do the work...
6. Return and mark: In Progress → Completed
7. System records completion time automatically
```

---

### Citizen (Public User)
| Feature | What It Does |
|---------|-------------|
| 🆘 Submit Complaint | Report problem to city government |
| 🔍 Track Status | Monitor complaint progress in real-time |
| 💰 View Bills | Check monthly utility charges |
| 💳 Pay Bills | Pay utility bills securely online |
| ⭐ Rate Service | Give feedback (1-5 stars) on complaint resolution |

**Example Citizen Workflow:**
```
1. Login as Citizen (Alice)
2. Submit complaint: "Streetlight broken on 5th Street"
3. Category: Street Maintenance
4. Priority: Normal
5. Submit → Get confirmation
6. Check status later: Assigned → In Progress → Resolved
7. Rate service: 4/5 stars
8. View & pay water bill: 2500 PKR
9. Receive payment confirmation
```

---

## 🔐 Authentication & Security

### How Passwords Are Protected

```
User enters password
         ↓
bcrypt.hashpw() [One-way encryption]
         ↓
Store hash in database (NOT password)
         ↓
Next login: Compare new password with stored hash
         ↓
Match = Login successful, No match = Access denied
```

**Why bcrypt?**
- Salt added automatically (prevents rainbow table attacks)
- One-way encryption (can't be reversed even by admins)
- Industry standard (used by Facebook, Netflix, etc.)

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MS SQL Server 2017 or higher
- ODBC Driver 17 for SQL Server
- pip (comes with Python)

### Step 1: Clone/Download Project
```bash
cd /path/to/Project_DBMS
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

Or use auto-installer:
```bash
python3 install_requirements.py
```

### Step 5: Set Up Database

**Option A: Using SQL Script**
```bash
sqlcmd -S localhost\SQLEXPRESS -i smart-city-management-system/database/smartcity.sql
```

**Option B: Manual (SQL Server Management Studio)**
1. Open SQL Server Management Studio
2. Create new database: `SmartCityDB`
3. Open file: `smart-city-management-system/database/smartcity.sql`
4. Click "Execute"
5. Wait for completion

### Step 6: Update Connection String

Edit `smart-city-management-system/db.py`:

```python
self.conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=YOUR_COMPUTER\\SQLEXPRESS;"     # Change to your SQL Server
    "DATABASE=SmartCityDB;"
    "Trusted_Connection=yes;"
)
```

For remote SQL Server:
```python
self.conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=192.168.1.100,1433;"
    "DATABASE=SmartCityDB;"
    "UID=sa;"
    "PWD=YourPassword123;"
)
```

### Step 7: Run Application
```bash
python smart-city-management-system/main.py
```

---

## 📁 Project Structure

```
Project_DBMS/
├── venv/                                    # Virtual environment
├── requirements.txt                         # Python dependencies
├── install_requirements.py                  # Auto installer script
├── setup.sh                                 # Linux/Mac setup script
├── SETUP_GUIDE.md                          # Setup instructions
├── README.md                                # This file
│
└── smart-city-management-system/
    ├── main.py                              # Application entry point
    │   └── Starts PyQt6 app, connects to DB
    │
    ├── db.py                                # Database manager
    │   ├── authenticate_user()              # Login verification
    │   ├── get_tasks()                      # Retrieve employee tasks
    │   ├── update_task_status()             # Update task progress
    │   ├── add_complaint()                  # Submit complaint
    │   ├── get_payments()                   # View bills
    │   ├── hash_password()                  # Bcrypt hashing
    │   └── verify_password()                # Password verification
    │
    ├── database/
    │   └── smartcity.sql                    # Complete database schema
    │       ├── CREATE TABLE employees
    │       ├── CREATE TABLE citizens
    │       ├── CREATE TABLE complaints
    │       ├── CREATE TABLE tasks
    │       ├── CREATE TABLE utilities
    │       ├── CREATE TABLE payments
    │       ├── CREATE TABLE departments
    │       ├── CREATE TABLE traffic_data
    │       └── CREATE TABLE waste_collection
    │
    └── ui/                                  # Frontend (PyQt6 GUI)
        ├── role_selector.py                 # Initial role selection
        │   └── 3 buttons: Admin/Employee/Citizen Login
        │
        ├── login.py                         # Shared login window
        │   ├── Username field
        │   ├── Password field
        │   └── Login button
        │
        ├── dashboard.py                     # Router component
        │   └── Directs to appropriate panel based on role
        │
        ├── admin_panel.py                   # Admin interface
        │   ├── Manage Complaints
        │   ├── Assign Tasks
        │   ├── Manage Employees
        │   └── View Analytics
        │
        ├── employee_panel.py                # Employee interface
        │   ├── View assigned tasks
        │   └── Update task status
        │
        ├── citizen_panel.py                 # Citizen interface
        │   ├── Submit complaints
        │   └── View & pay bills
        │
        └── __pycache__/                     # Compiled bytecode (auto-generated)
```

---

## 🚀 How to Use

### First Time Setup

**For Admin:**
1. Run: `python smart-city-management-system/main.py`
2. Click "Login as Admin"
3. Enter: admin / password
4. View the Admin Dashboard
5. Explore: Complaints → Tasks → Employees → Analytics

**For Employee:**
1. Click "Login as Employee"
2. Enter your employee credentials
3. View assigned tasks
4. Click task to see details
5. Change status: Pending → In Progress → Completed

**For Citizen:**
1. Click "Login as Citizen"
2. Register or login with existing account
3. Submit complaint (e.g., "Broken streetlight")
4. View your bills
5. Click to pay any bills
6. Track complaint status in real-time

---

## 🛠️ Development Guide

### Adding a New Feature

**Example: Add "Export to PDF" for complaints**

**Step 1: Database Method** (`db.py`)
```python
def get_complaint_details(self, complaint_id):
    try:
        self.cursor.execute("""
            SELECT complaint_id, title, description, status, submitted_at
            FROM complaints WHERE complaint_id = ?
        """, (complaint_id,))
        return self.cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        return None
```

**Step 2: UI Button** (`ui/admin_panel.py`)
```python
self.btn_export = QPushButton("Export to PDF")
self.btn_export.clicked.connect(self.export_complaint)
self.layout_main.addWidget(self.btn_export)
```

**Step 3: Connect Signal** (`ui/admin_panel.py`)
```python
def export_complaint(self):
    complaint_id = self.complaint_list.currentItem().data(Qt.UserRole)
    data = db.get_complaint_details(complaint_id)
    # Generate PDF from data
    QMessageBox.information(self, "Success", "PDF exported!")
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt6'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "❌ DB Connection failed"
1. Verify SQL Server is running
2. Check connection string in `db.py`
3. Verify database exists: `SELECT name FROM sys.databases`
4. Check ODBC drivers: `odbcad32.exe` (Windows)

### "Login failed"
1. Verify username and password are correct
2. Check employee/citizen record exists
3. Ensure user is active (is_active = 1)
4. Verify database has required tables

---

## 📈 Key Metrics

- **Supported Users**: Unlimited
- **Data Storage**: Depends on SQL Server
- **Response Time**: < 1 second (queries)
- **Concurrent Connections**: Up to database limit
- **Security**: Bcrypt hashing + SQL Server encryption

---

## ✅ Deployment Checklist

Before going live:

- [ ] All users have secure bcrypt passwords
- [ ] Database backups configured
- [ ] ODBC driver installed on all client machines
- [ ] Connection string uses secure credentials
- [ ] Test with sample data works
- [ ] Employee roles properly configured
- [ ] Entire workflow tested end-to-end
- [ ] Error handling catches all edge cases

---

## 📞 Support

- **Python Issues**: Check Python version (3.8+)
- **Database Issues**: Verify SQL Server is running and accessible
- **PyQt6 Issues**: Reinstall: `pip install --upgrade PyQt6`
- **Connection Issues**: Update connection string in `db.py`

---

**Version**: 1.0  
**Status**: Production Ready ✅  
**Last Updated**: May 7, 2026

