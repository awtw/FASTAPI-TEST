import logging
import os
import sys
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""

    # ANSI escape codes for colors
    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[31;1m'  # Red + Bold
    }
    RESET = '\033[0m'

    def __init__(self, fmt=None, datefmt=None, use_colors=True):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors and sys.stdout.isatty()  # Only use colors if output is a terminal

    def format(self, record):
        if self.use_colors and record.levelname in self.COLORS:
            # Save original levelname
            levelname_original = record.levelname
            # Add color to levelname
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            # Format the message
            formatted = super().format(record)
            # Restore original levelname
            record.levelname = levelname_original
            return formatted
        return super().format(record)


def wrap_logger(logger: logging.Logger, file_name: Optional[str] = None):
    """
    Wraps a logger with custom formatting.
    
    Sentry integration is automatically enabled globally via LoggingIntegration in server.py.
    All logs from this logger will be automatically captured by Sentry if configured.
    
    Args:
        logger: The logger instance to wrap
        file_name: Optional file path to write logs to
    
    Returns:
        The configured logger instance
    """
    # Check if handlers already exist to avoid duplicates
    if logger.handlers:
        return logger

    # Get log level from environment variable, default to INFO
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    numeric_level = getattr(logging, log_level, logging.INFO)
    logger.setLevel(numeric_level)

    # Prevent propagation to avoid duplicate logs from parent loggers
    logger.propagate = False

    stream_handler = logging.StreamHandler(sys.stdout)

    # Use ColoredFormatter for console output
    colored_formatter = ColoredFormatter(
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s",
        use_colors=True
    )
    stream_handler.setFormatter(colored_formatter)
    logger.addHandler(stream_handler)

    # add file handler (without colors)
    if file_name is not None:
        file_handler = logging.FileHandler(file_name)
        # Use regular formatter for file output (no colors)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
