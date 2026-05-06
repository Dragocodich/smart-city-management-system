import pyodbc

# ───── CONFIG ─────
USE_DEMO_MODE = False


class DatabaseManager:
    def __init__(self):
        self.demo = USE_DEMO_MODE
        self.conn = None
        self.cursor = None

    # ───── CONNECT ─────
    def connect(self):
        if self.demo:
            print("🟡 Demo mode active")
            return

        try:
            self.conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=DESKTOP-62TRPPU\\SQLEXPRESS;"
                "DATABASE=SmartCityDB;"
                "Trusted_Connection=yes;"
                "Connection Timeout=10;"
            )

            self.cursor = self.conn.cursor()
            print("✅ Connected to SmartCityDB successfully!")

        except Exception as e:
            print("❌ Database connection failed:", e)

    # ───── LOGIN ─────
    def authenticate_user(self, username, password):

        if self.demo:
            if username == "admin" and password == "Admin@123":
                return {
                    "type": "employee",
                    "data": {
                        "emp_id": 1,
                        "role": "admin",
                        "full_name": "System Admin"
                    }
                }
            return None

        try:
            query = """
                SELECT emp_id, role, full_name
                FROM employees
                WHERE username = ? AND password_hash = ?
            """

            self.cursor.execute(query, (username, password))
            row = self.cursor.fetchone()

            if row:
                return {
                    "type": "employee",
                    "data": {
                        "emp_id": row[0],
                        "role": row[1],
                        "full_name": row[2]
                    }
                }

            return None

        except Exception as e:
            print("❌ Login error:", e)
            return None

    # ───── GET COMPLAINTS ─────
    def get_complaints(self):
        try:
            query = """
                SELECT complaint_id, title, status, priority
                FROM complaints
                ORDER BY submitted_at DESC
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Exception as e:
            print("❌ get_complaints error:", e)
            return []

    # ───── ASSIGN TASK ─────
    def assign_task(self, complaint_id, dept_id, assigned_to,
                    assigned_by, title, priority, due_date):

        try:
            query = """
                INSERT INTO tasks
                (complaint_id, dept_id, assigned_to, assigned_by, title, priority, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(query, (
                complaint_id,
                dept_id,
                assigned_to,
                assigned_by,
                title,
                priority,
                due_date
            ))

            self.conn.commit()
            print("✅ Task assigned successfully")

        except Exception as e:
            print("❌ assign_task error:", e)

    # ───── CLOSE ─────
    def close(self):
        if self.conn:
            self.conn.close()
            print("🔌 Database connection closed")


# ───── GLOBAL INSTANCE ─────
db = DatabaseManager()