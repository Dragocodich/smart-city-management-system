# ============================================================
# REFACTORED DATABASE MANAGER - CORE MODULE
# ============================================================

try:
    import pyodbc
except ImportError:
    pyodbc = None

import bcrypt
from config.database_config import CONNECTION_STRING
from utils.logger import Logger
from utils.exceptions import DatabaseException, AuthenticationException

class DatabaseManager:
    """Centralized database management"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize database manager"""
        self.conn = None
        self.cursor = None
        self.logger = Logger()
        
        # ──────────────────────────────────────────────
        # MOCK DATABASE FOR DEVELOPMENT MODE
        # ──────────────────────────────────────────────
        # Format: username -> (password, role, full_name, id)
        self.mock_employees = {
            'admin': {
                'password': 'Admin@123',
                'role': 'admin',
                'full_name': 'System Administrator',
                'emp_id': 1
            },
            'worker1': {
                'password': 'Worker@123',
                'role': 'worker',
                'full_name': 'Field Worker',
                'emp_id': 2
            },
            'officer1': {
                'password': 'Officer@123',
                'role': 'officer',
                'full_name': 'Traffic Officer',
                'emp_id': 3
            }
        }
        
        self.mock_citizens = {
            'citizen1': {
                'password': 'Citizen@123',
                'full_name': 'Ali Khan',
                'citizen_id': 1
            }
        }

    # ─────────────────────────────
    # CONNECTION MANAGEMENT
    # ─────────────────────────────

    def connect(self):
        """Connect to database"""
        if pyodbc is None:
            self.logger.warning("PyODBC not available. Database operations will fail.")
            return False
            
        try:
            self.conn = pyodbc.connect(CONNECTION_STRING)
            self.cursor = self.conn.cursor()
            self.logger.info("✅ Connected to SmartCityDB successfully!")
            return True
        except Exception as e:
            error_msg = f"DB Connection failed: {e}"
            self.logger.error(error_msg)
            raise DatabaseException(error_msg)

    def disconnect(self):
        """Disconnect from database"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            self.logger.info("Database disconnected")
        except pyodbc.Error as e:
            self.logger.error(f"Error disconnecting: {e}")

    def reconnect(self):
        """Reconnect to database"""
        self.disconnect()
        self.connect()

    # ─────────────────────────────
    # QUERY EXECUTION
    # ─────────────────────────────

    def execute_query(self, query, params=None):
        """Execute SELECT query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            error_msg = f"Query execution failed: {e}"
            self.logger.error(error_msg)
            raise DatabaseException(error_msg)

    def execute_single(self, query, params=None):
        """Execute SELECT query and return single row"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Exception as e:
            error_msg = f"Query execution failed: {e}"
            self.logger.error(error_msg)
            raise DatabaseException(error_msg)

    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            self.logger.info(f"Query updated {self.cursor.rowcount} row(s)")
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            error_msg = f"Update query failed: {e}"
            self.logger.error(error_msg)
            raise DatabaseException(error_msg)

    def execute_batch(self, query, params_list):
        """Execute batch INSERT/UPDATE"""
        try:
            self.cursor.executemany(query, params_list)
            self.conn.commit()
            self.logger.info(f"Batch updated {self.cursor.rowcount} row(s)")
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            error_msg = f"Batch execution failed: {e}"
            self.logger.error(error_msg)
            raise DatabaseException(error_msg)

    # ─────────────────────────────
    # PASSWORD MANAGEMENT
    # ─────────────────────────────

    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(
                password.encode(),
                hashed.encode()
            )
        except Exception as e:
            Logger().error(f"Password verification failed: {e}")
            return False

    # ─────────────────────────────
    # AUTHENTICATION
    # ─────────────────────────────

    def authenticate_user(self, username, password, role):
        """Authenticate user based on role"""
        try:
            # Map "employee" UI role to valid database roles
            if role == "employee":
                # Default generic "employee" role to "worker" for development
                role = "worker"
            
            if role in ["admin", "officer", "worker", "emergency"]:
                return self._authenticate_employee(username, password, role)
            elif role == "citizen":
                return self._authenticate_citizen(username, password)
            else:
                raise AuthenticationException(f"Unknown role: {role}")
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            raise

    def _authenticate_employee(self, username, password, role):
        """Authenticate employee - with fallback to mock mode"""
        
        # IF DATABASE AVAILABLE, USE IT
        if self.conn is not None:
            query = """
                SELECT emp_id, role, full_name, password_hash
                FROM employees
                WHERE username = ? AND is_active = 1
            """
            try:
                row = self.execute_single(query, (username,))
                if row:
                    if self.verify_password(password, row[3]):
                        self.logger.info(f"✅ Employee {username} authenticated via database")
                        return {
                            "type": "employee",
                            "data": {
                                "emp_id": row[0],
                                "role": row[1],
                                "full_name": row[2]
                            }
                        }
                    else:
                        self.logger.warning(f"Employee {username} found but password incorrect")
                else:
                    self.logger.warning(f"Employee {username} not found in database (or inactive)")
            except Exception as e:
                self.logger.warning(f"Database query failed for employee auth, falling back to dev mode: {e}")
        
        # FALLBACK: USE MOCK AUTHENTICATION (DEVELOPMENT MODE)
        self.logger.info(f"Attempting mock/dev mode authentication for employee {username}")
        if username in self.mock_employees:
            mock_user = self.mock_employees[username]
            if mock_user['password'] == password:
                self.logger.info(f"✅ {username} authenticated in DEV MODE (role: {mock_user['role']})")
                return {
                    "type": "employee",
                    "data": {
                        "emp_id": mock_user['emp_id'],
                        "role": mock_user['role'],
                        "full_name": mock_user['full_name']
                    }
                }
            else:
                self.logger.warning(f"Employee {username} found in mock data but password incorrect")
        else:
            self.logger.warning(f"Employee {username} not found in mock data. Available: {list(self.mock_employees.keys())}")
        
        raise AuthenticationException("Invalid credentials")

    def _authenticate_citizen(self, username, password):
        """Authenticate citizen - with fallback to mock mode"""
        
        # IF DATABASE AVAILABLE, USE IT
        if self.conn is not None:
            query = """
                SELECT citizen_id, full_name, password_hash
                FROM citizens
                WHERE username = ? AND is_active = 1
            """
            try:
                row = self.execute_single(query, (username,))
                if row:
                    if self.verify_password(password, row[2]):
                        return {
                            "type": "citizen",
                            "data": {
                                "citizen_id": row[0],
                                "full_name": row[1]
                            }
                        }
            except Exception as e:
                self.logger.warning(f"Database query failed, falling back to dev mode: {e}")
        
        # FALLBACK: USE MOCK AUTHENTICATION (DEVELOPMENT MODE)
        if username in self.mock_citizens:
            mock_user = self.mock_citizens[username]
            if mock_user['password'] == password:
                self.logger.info(f"✅ {username} authenticated in DEV MODE")
                return {
                    "type": "citizen",
                    "data": {
                        "citizen_id": mock_user['citizen_id'],
                        "full_name": mock_user['full_name']
                    }
                }
        
        raise AuthenticationException("Invalid credentials")

    # ─────────────────────────────
    # TRANSACTION MANAGEMENT
    # ─────────────────────────────

    def begin_transaction(self):
        """Start transaction"""
        self.conn.execute("BEGIN TRANSACTION")
        self.logger.info("Transaction started")

    def commit_transaction(self):
        """Commit transaction"""
        self.conn.commit()
        self.logger.info("Transaction committed")

    def rollback_transaction(self):
        """Rollback transaction"""
        self.conn.rollback()
        self.logger.info("Transaction rolled back")


# Singleton instance
db = DatabaseManager()
