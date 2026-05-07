import pyodbc
import bcrypt


class DatabaseManager:

    def __init__(self):
        self.conn = None
        self.cursor = None

    # ─────────────────────────────
    # CONNECT DATABASE
    # ─────────────────────────────
    def connect(self):

        try:

            self.conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=DESKTOP-62TRPPU\\SQLEXPRESS;"
                "DATABASE=SmartCityDB;"
                "Trusted_Connection=yes;"
            )

            self.cursor = self.conn.cursor()

            print("✅ Connected to SmartCityDB successfully!")

        except Exception as e:
            print("❌ DB Connection failed:", e)

    # ─────────────────────────────
    # PASSWORD HASH
    # ─────────────────────────────
    def hash_password(self, password):

        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

    # ─────────────────────────────
    # VERIFY PASSWORD
    # ─────────────────────────────
    def verify_password(self, password, hashed):

        try:
            return bcrypt.checkpw(
                password.encode(),
                hashed.encode()
            )
        except:
            return False

    # ─────────────────────────────
    # AUTH (KEEP YOUR EXISTING ONE IF WORKING)
    # ─────────────────────────────
    def authenticate_user(self, username, password, role):

        try:

            if role in ["admin", "employee"]:

                self.cursor.execute("""
                    SELECT emp_id, role, full_name, password_hash
                    FROM employees
                    WHERE username = ?
                """, (username,))

                row = self.cursor.fetchone()

                if row:

                    if self.verify_password(password, row[3]):

                        return {
                            "type": "employee",
                            "data": {
                                "emp_id": row[0],
                                "role": row[1],
                                "full_name": row[2]
                            }
                        }

            elif role == "citizen":

                self.cursor.execute("""
                    SELECT citizen_id, full_name, password_hash
                    FROM citizens
                    WHERE username = ?
                """, (username,))

                row = self.cursor.fetchone()

                if row:

                    if self.verify_password(password, row[2]):

                        return {
                            "type": "citizen",
                            "data": {
                                "citizen_id": row[0],
                                "full_name": row[1]
                            }
                        }

            return None

        except Exception as e:
            print("❌ Login error:", e)
            return None

    # ─────────────────────────────
    # GET TASKS ⭐ FIXED (YOUR ERROR)
    # ─────────────────────────────
    def get_tasks(self, filters):

        try:

            emp_id = filters.get("assigned_to")

            self.cursor.execute("""
                SELECT task_id, title, status
                FROM tasks
                WHERE assigned_to = ?
                ORDER BY task_id DESC
            """, (emp_id,))

            rows = self.cursor.fetchall()

            return [
                {
                    "task_id": r[0],
                    "title": r[1],
                    "status": r[2]
                }
                for r in rows
            ]

        except Exception as e:
            print("❌ get_tasks error:", e)
            return []

    # ─────────────────────────────
    # UPDATE TASK STATUS ⭐ FIXED
    # ─────────────────────────────
    def update_task_status(self, task_id, status):

        try:

            self.cursor.execute("""
                UPDATE tasks
                SET status = ?
                WHERE task_id = ?
            """, (status, task_id))

            self.conn.commit()

        except Exception as e:
            print("❌ update_task_status error:", e)

    # ─────────────────────────────
    # ADD COMPLAINT
    # ─────────────────────────────
    def add_complaint(self, citizen_id, dept_id, title, desc, category, priority, location):

        try:

            self.cursor.execute("""
                INSERT INTO complaints
                (citizen_id, dept_id, title, description, category, priority, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (citizen_id, dept_id, title, desc, category, priority, location))

            self.conn.commit()

        except Exception as e:
            print("❌ add_complaint error:", e)

    # ─────────────────────────────
    # GET PAYMENTS
    # ─────────────────────────────
    def get_payments(self, citizen_id):

        try:

            self.cursor.execute("""
                SELECT payment_id, payment_type, status
                FROM payments
                WHERE citizen_id = ?
            """, (citizen_id,))

            rows = self.cursor.fetchall()

            return [
                {
                    "payment_id": r[0],
                    "payment_type": r[1],
                    "status": r[2]
                }
                for r in rows
            ]

        except Exception as e:
            print("❌ get_payments error:", e)
            return []

    # ─────────────────────────────
    # PAY BILL
    # ─────────────────────────────
    def pay_bill(self, payment_id):

        try:

            self.cursor.execute("""
                UPDATE payments
                SET status = 'Paid',
                    paid_at = GETDATE()
                WHERE payment_id = ?
            """, (payment_id,))

            self.conn.commit()

        except Exception as e:
            print("❌ pay_bill error:", e)

    # ─────────────────────────────
    # CLOSE CONNECTION
    # ─────────────────────────────
    def close(self):

        if self.conn:
            self.conn.close()


# GLOBAL INSTANCE
db = DatabaseManager()