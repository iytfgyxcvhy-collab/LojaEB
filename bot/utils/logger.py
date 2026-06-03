"""
Logger configuration for LojaEB bot.
Centralized logging system with file and console output.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """Centralized logging system."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.setup_logging()

    def setup_logging(self):
        """Configure logging system."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE", f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log")

        # Create logger
        self.logger = logging.getLogger("LojaEB")
        self.logger.setLevel(getattr(logging, log_level))

        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(getattr(logging, log_level))

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level))

        # Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self, name: str = None):
        """Get logger instance."""
        if name:
            return logging.getLogger(f"LojaEB.{name}")
        return self.logger

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def error(self, message: str, exc_info: bool = False):
        """Log error message."""
        self.logger.error(message, exc_info=exc_info)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)


# Singleton instance
logger_instance = Logger()

def get_logger(name: str = None):
    """Get logger instance."""
    return logger_instance.get_logger(name)
