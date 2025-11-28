"""
Logging configuration for the application.
"""

import logging
import sys
from datetime import datetime

# Create logger
logger = logging.getLogger("codebloom")
logger.setLevel(logging.INFO)

# Create console handler with formatting
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

# Prevent duplicate logs
logger.propagate = False


def log_request(endpoint: str, method: str, user_message: str = None):
    """Log incoming API requests."""
    if user_message:
        logger.info(f"{method} {endpoint} - Message: {user_message[:50]}...")
    else:
        logger.info(f"{method} {endpoint}")


def log_response(endpoint: str, status: str, duration_ms: float = None):
    """Log API responses."""
    if duration_ms:
        logger.info(f"{endpoint} - Status: {status} - Duration: {duration_ms:.2f}ms")
    else:
        logger.info(f"{endpoint} - Status: {status}")


def log_error(endpoint: str, error: Exception):
    """Log errors."""
    logger.error(f"{endpoint} - Error: {type(error).__name__}: {str(error)}")


def log_warning(message: str):
    """Log warnings."""
    logger.warning(message)


def log_info(message: str):
    """Log informational messages."""
    logger.info(message)
