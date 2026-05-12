# Setup Instructions

## Quick Start Guide

Follow these steps to set up and run the Smart City Management System after cloning the repository.

### Prerequisites
- Python 3.8 or higher
- SQL Server (with ODBC driver installed)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Project_DBMS
```

### 2. Create Virtual Environment
```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database Connection
1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your SQL Server credentials:
```
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_SERVER=your_server_name\SQLEXPRESS
DB_NAME=SmartCityDB
DB_TRUSTED=yes
```

### 5. Set Up Database
1. Open SQL Server Management Studio (SSMS) or any SQL editor
2. Run the SQL script to create the database:
```
smart-city-management-system/database/smartcity.sql
```

### 6. Run the Application
```bash
cd smart-city-management-system
python main.py
```

### Alternative: Automated Setup (Linux/macOS)
Run the setup script to automatically create a virtual environment and install dependencies:
```bash
chmod +x setup.sh
./setup.sh
```

Then configure the database as described in steps 4 and 5.

## Troubleshooting

### Database Connection Issues
- Ensure SQL Server is running
- Verify ODBC driver is installed: `odbcinst -j`
- Check connection string in `.env` file
- Confirm database user has proper permissions

### PyQt6 Issues (on Linux)
If you encounter display issues:
```bash
sudo apt-get install python3-pyqt6
```

### Import Errors
Make sure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Default Login Credentials
After database setup, use these test credentials:

**Admin:**
- Username: `admin`
- Password: `admin123`

**Employee:**
- Username: `emp1`
- Password: `emp123`

**Citizen:**
- Username: `citizen1`
- Password: `citizen123`

⚠️ Change these credentials in production!

## Project Structure
```
smart-city-management-system/
├── main.py              # Application entry point
├── config/              # Configuration files
├── core/                # Core database functionality
├── database/            # Database schema (smartcity.sql)
├── services/            # Business logic services
├── ui/                  # UI components (PyQt6)
├── utils/               # Utilities and helpers
└── logs/                # Application logs (auto-generated)
```

## Support
For issues or questions, refer to the README.md file or check the logs in `smart-city-management-system/logs/`
