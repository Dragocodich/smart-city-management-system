# ============================================================
# LOGGING UTILITY
# ============================================================

import logging
import os
from datetime import datetime

class Logger:
    """Centralized logging system"""

    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize logger"""
        log_dir = os.path.join(os.path.dirname(__file__), '../logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self._logger = logging.getLogger(__name__)

    def info(self, message):
        """Log info message"""
        self._logger.info(message)

    def warning(self, message):
        """Log warning message"""
        self._logger.warning(message)

    def error(self, message):
        """Log error message"""
        self._logger.error(message)

    def debug(self, message):
        """Log debug message"""
        self._logger.debug(message)

    def critical(self, message):
        """Log critical message"""
        self._logger.critical(message)
