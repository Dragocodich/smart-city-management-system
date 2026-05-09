from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QIcon, QPixmap
from core.database import db
from utils.exceptions import AuthenticationException
from utils.logger import Logger


class LoginWindow(QWidget):

    def __init__(self, role, role_selector=None):
        super().__init__()

        # SAVE ROLE AND REFERENCE
        self.role = role
        self.role_selector = role_selector
        self.logger = Logger()

        # WINDOW SETTINGS
        self.setWindowTitle(f"Smart City - {role.capitalize()} Login")
        self.setGeometry(300, 100, 900, 600)
        self.setMinimumSize(900, 600)
        
        # WINDOW ICON (optional: can be replaced with actual icon)
        self.setWindowFlag(Qt.WindowType.Window)

        # MAIN CONTAINER
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ──────────────────────────────────────
        # LEFT SIDE - BRANDING
        # ──────────────────────────────────────
        left_panel = QWidget()
        left_panel.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
        """)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 20, 20, 20)
        
        # BACK BUTTON
        back_btn = QPushButton("← Back")
        back_btn.setMaximumWidth(100)
        back_btn.setMinimumHeight(35)
        back_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                border-radius: 6px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        back_btn.clicked.connect(self.go_back)
        left_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # LOGO/ICON
        logo_label = QLabel("🏙️")
        logo_label.setFont(QFont("Arial", 64, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # BRAND TEXT
        brand = QLabel("Smart City\nManagement System")
        brand.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setStyleSheet("color: white; line-height: 1.5;")

        # TAGLINE
        tagline = QLabel("Making cities smarter, cleaner, safer")
        tagline.setFont(QFont("Arial", 12))
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-style: italic;
        """)

        left_layout.addWidget(logo_label)
        left_layout.addSpacing(20)
        left_layout.addWidget(brand)
        left_layout.addSpacing(10)
        left_layout.addWidget(tagline)
        left_layout.addStretch()

        left_panel.setLayout(left_layout)

        # ──────────────────────────────────────
        # RIGHT SIDE - LOGIN FORM
        # ──────────────────────────────────────
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(20)

        # ROLE TITLE
        role_title = QLabel(f"{role.capitalize()} Login Portal")
        role_title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        role_title.setStyleSheet("color: #2c3e50;")
        role_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # SUBTITLE
        subtitle = QLabel("Sign in to continue")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # SEPARATOR
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #ecf0f1;")

        # USERNAME SECTION
        username_label = QLabel("Username")
        username_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #34495e;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setMinimumHeight(45)
        self.username.setFont(QFont("Arial", 11))
        self.username.setStyleSheet(self._get_input_style())
        self.username.returnPressed.connect(self.login)

        # PASSWORD SECTION
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #34495e;")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setMinimumHeight(45)
        self.password.setFont(QFont("Arial", 11))
        self.password.setStyleSheet(self._get_input_style())
        self.password.returnPressed.connect(self.login)

        # REMEMBER ME & FORGOT PASSWORD
        checkbox_layout = QHBoxLayout()
        self.remember_me = QCheckBox("Remember me")
        self.remember_me.setFont(QFont("Arial", 10))
        self.remember_me.setStyleSheet("color: #34495e;")

        forgot_pwd = QPushButton("Forgot password?")
        forgot_pwd.setFlat(True)
        forgot_pwd.setFont(QFont("Arial", 10))
        forgot_pwd.setCursor(Qt.CursorShape.PointingHandCursor)
        forgot_pwd.setStyleSheet("""
            QPushButton {
                color: #3498db;
                text-decoration: underline;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                color: #2980b9;
            }
        """)

        checkbox_layout.addWidget(self.remember_me)
        checkbox_layout.addStretch()
        checkbox_layout.addWidget(forgot_pwd)

        # LOGIN BUTTON
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet(self._get_button_style())
        self.login_btn.clicked.connect(self.login)

        # STATUS MESSAGE
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setFont(QFont("Arial", 10))
        self.status.setWordWrap(True)
        self.status.setMinimumHeight(20)

        # INFO BOX
        info_box = QGroupBox("Demo Credentials (Development Mode)")
        info_layout = QVBoxLayout()
        info_text = QLabel(
            "👤 Admin:\n"
            "   Username: admin\n"
            "   Password: Admin@123\n\n"
            "👷 Worker:\n"
            "   Username: worker1\n"
            "   Password: Worker@123\n\n"
            "👨‍⚖️ Citizen:\n"
            "   Username: citizen1\n"
            "   Password: Citizen@123"
        )
        info_text.setFont(QFont("Arial", 9))
        info_text.setStyleSheet("color: #7f8c8d;")
        info_layout.addWidget(info_text)
        info_box.setLayout(info_layout)
        info_box.setStyleSheet("""
            QGroupBox {
                color: #7f8c8d;
                border: 1px solid #ecf0f1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0px 3px 0px 3px;
            }
        """)

        # ADD TO RIGHT LAYOUT
        right_layout.addWidget(role_title)
        right_layout.addWidget(subtitle)
        right_layout.addWidget(line)
        right_layout.addSpacing(10)
        right_layout.addWidget(username_label)
        right_layout.addWidget(self.username)
        right_layout.addWidget(password_label)
        right_layout.addWidget(self.password)
        right_layout.addLayout(checkbox_layout)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.login_btn)
        right_layout.addWidget(self.status)
        right_layout.addWidget(info_box)
        right_layout.addStretch()

        right_panel.setLayout(right_layout)
        right_panel.setStyleSheet("background-color: white;")

        # COMBINE PANELS
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget = lambda w: None  # Dummy for QWidget
        self.setLayout(main_layout)

    def _get_input_style(self):
        """Return styling for input fields"""
        return """
            QLineEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 10px 15px;
                background-color: white;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #f8f9fa;
            }
            QLineEdit:hover {
                border: 2px solid #bdc3c7;
            }
        """

    def _get_button_style(self):
        """Return styling for login button"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980b9, stop:1 #1f618d);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1f618d, stop:1 #154360);
            }
        """


    # ─────────────────────────────
    # LOGIN FUNCTION
    # ─────────────────────────────
    def login(self):

        username = self.username.text().strip()
        password = self.password.text().strip()

        # EMPTY CHECK
        if not username or not password:
            self._show_error("⚠ Please fill all fields")
            self.logger.warning(f"Login attempt with empty credentials for role: {self.role}")
            return

        # DISABLE BUTTON DURING LOGIN
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Signing in...")

        try:
            # AUTHENTICATE USER
            user = db.authenticate_user(
                username,
                password,
                self.role
            )

            # SUCCESS
            self._show_success("✅ Login successful")
            self.logger.info(f"User {username} ({self.role}) logged in successfully")
            
            # STORE REMEMBER ME
            if self.remember_me.isChecked():
                self.logger.info(f"Remember me enabled for {username}")

            # DELAY THEN OPEN DASHBOARD
            QTimer.singleShot(800, lambda: self.open_dashboard(user))

        except AuthenticationException as e:
            # Check if it's an employee login failure
            if self.role == "employee":
                help_msg = "\n\n💡 Demo Employees:\nUsername: worker1 | Pass: Worker@123\nUsername: officer1 | Pass: Officer@123\n\n(Note: 'employee' role maps to 'worker' for authentication)"
                self._show_error(f"❌ Login failed\n{help_msg}")
                self.logger.warning(f"Failed employee login for user: {username}")
            else:
                self._show_error("❌ Invalid username or password")
                self.logger.warning(f"Failed {self.role} login attempt for user: {username}")
        except Exception as e:
            error_msg = str(e)
            if "Database" in error_msg or "pyodbc" in error_msg.lower():
                self._show_error("ℹ️  Development Mode - Use demo credentials\n(No database connection)")
                self.logger.info(f"Dev mode - check credentials in info box")
            else:
                self._show_error(f"❌ Login error: {str(e)[:30]}...")
            self.logger.error(f"Login error: {e}")
        finally:
            # RE-ENABLE BUTTON
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Sign In")

    def _show_error(self, message):
        """Show error message with red styling"""
        self.status.setText(message)
        self.status.setStyleSheet("""
            color: #e74c3c;
            font-weight: bold;
        """)

    def _show_success(self, message):
        """Show success message with green styling"""
        self.status.setText(message)
        self.status.setStyleSheet("""
            color: #27ae60;
            font-weight: bold;
        """)

    # ─────────────────────────────
    # GO BACK TO ROLE SELECTOR
    # ─────────────────────────────
    def go_back(self):
        """Go back to role selector"""
        self.logger.info(f"User cancelled {self.role} login and returned to role selector")
        if self.role_selector:
            self.role_selector.show()
        self.close()

    # ─────────────────────────────
    # OPEN DASHBOARD
    # ─────────────────────────────
    def open_dashboard(self, user):

        from ui.dashboard import Dashboard

        def on_logout():
            """Callback when user logs out from dashboard"""
            # Show login window again
            self.show()
            # Clear the password field
            self.password.setText("")
            self.username.setText("")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("🔓 Login")

        self.dashboard = Dashboard(user, on_logout)
        self.dashboard.show()
        # Hide (don't close) the login window so we can return to it after logout
        self.hide()