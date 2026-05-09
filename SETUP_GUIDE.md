# Smart City Management System - Setup Guide

## 📋 Overview
This guide will help you set up the Smart City Management System with all required dependencies in a virtual environment.

## 🔧 Requirements
- Python 3.8 or higher
- pip (Python package manager)

## 📦 Required Libraries
- **PyQt6** - GUI framework for the user interface
- **pyodbc** - Database connectivity for SQL Server
- **bcrypt** - Password hashing and verification

These are all listed in `requirements.txt` for easy installation.

---

## ✅ Quick Setup

### Option 1: Automatic Setup (Recommended for Linux/Mac)

Run the automatic setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
1. Create a virtual environment if it doesn't exist
2. Activate the virtual environment
3. Install all required packages from `requirements.txt`
4. Display instructions for running the application

### Option 2: Using Python Script (All Platforms)

Run the Python install script:

```bash
python3 install_requirements.py
```

This script will:
1. Create a virtual environment if it doesn't exist
2. Install all packages from `requirements.txt`
3. Show you the activation command for your system

### Option 3: Manual Setup

If you prefer manual setup, follow these steps:

#### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
```

#### Step 2: Activate Virtual Environment
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```cmd
  venv\Scripts\activate
  ```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

After setup, make sure your virtual environment is activated, then run:

```bash
python main.py
```

---

## 📝 Managing Dependencies

### Adding New Packages

If you need to add new packages to your project:

1. Install the package in the virtual environment:
   ```bash
   pip install package_name
   ```

2. Update `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

3. Commit the updated `requirements.txt` to version control

### Viewing Installed Packages

To see all packages installed in your virtual environment:

```bash
pip list
```

To see packages from requirements.txt:

```bash
pip freeze
```

---

## 🔄 Reinstalling Dependencies

If you need to reinstall all dependencies:

1. Activate the virtual environment
2. Run:
   ```bash
   pip install --upgrade --force-reinstall -r requirements.txt
   ```

---

## ⚙️ Virtual Environment Management

### Deactivating the Virtual Environment
Simply run:
```bash
deactivate
```

### Removing the Virtual Environment
If you want to delete the virtual environment and start fresh:
```bash
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

Then recreate it using the steps above.

---

## 🐛 Troubleshooting

### Issue: "pip: command not found"
**Solution:** Make sure you're in the virtual environment. Activate it with:
- Linux/Mac: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

### Issue: "pyodbc won't install"
**Solution:** On Linux, you may need to install ODBC driver first:
```bash
# Ubuntu/Debian
sudo apt-get install unixodbc-dev

# Fedora
sudo dnf install unixODBC-devel
```

### Issue: "ModuleNotFoundError: No module named 'PyQt6'"
**Solution:** Ensure the virtual environment is activated and packages are installed:
```bash
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

---

## 📄 File Structure

```
smart-city-management-system/
├── venv/                           # Virtual environment (created after setup)
├── requirements.txt                # List of all dependencies
├── install_requirements.py         # Python installation script
├── setup.sh                        # Shell script for Linux/Mac
├── main.py                         # Main application entry point
├── db.py                          # Database manager
├── database/
│   └── smartcity.sql             # SQL database schema
└── ui/
    ├── login.py                   # Login window
    ├── role_selector.py          # Role selection screen
    ├── admin_panel.py            # Admin dashboard
    ├── employee_panel.py         # Employee dashboard
    ├── citizen_panel.py          # Citizen dashboard
    └── dashboard.py              # Main dashboard
```

---

## ✨ Features After Setup

Once everything is installed, you'll have access to:
- ✅ GUI application with PyQt6
- ✅ SQL Server database connectivity
- ✅ Secure password management with bcrypt
- ✅ Role-based access control (Admin, Employee, Citizen)

---

## 📞 Support

For issues or questions related to dependencies, check the official documentation:
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)
- [bcrypt Documentation](https://github.com/pyca/bcrypt)

---

**Happy coding! 🎉**
