import sys
from PyQt6.QtWidgets import QApplication

from core.database import db
from ui.role_selector import RoleSelector
from utils.logger import Logger


def main():
    """Main application entry point"""
    try:
        # Initialize application
        app = QApplication(sys.argv)
        logger = Logger()
        
        # Connect to database
        logger.info("Starting Smart City Management System...")
        db.connect()
        logger.info("Database connection established")
        
        # Show role selector window
        window = RoleSelector()
        window.show()
        
        # Run application
        logger.info("Application launched successfully")
        sys.exit(app.exec())
        
    except Exception as e:
        Logger().error(f"Application failed to start: {e}")
        raise


if __name__ == "__main__":
    main()