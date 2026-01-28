"""Centralized logging utility for Antigravity Workspace.

This module provides a consistent logging interface across the entire application
with support for multiple handlers, structured logging, and contextual information.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


# ANSI color codes for console output
class LogColors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Log level colors
    DEBUG = "\033[36m"      # Cyan
    INFO = "\033[32m"       # Green
    WARNING = "\033[33m"    # Yellow
    ERROR = "\033[31m"      # Red
    CRITICAL = "\033[35m"   # Magenta
    
    # Component colors
    AGENT = "\033[94m"      # Light Blue
    SWARM = "\033[95m"      # Light Magenta
    TOOL = "\033[96m"       # Light Cyan
    MCP = "\033[93m"        # Light Yellow


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to console output."""
    
    FORMATS = {
        logging.DEBUG: f"{LogColors.DEBUG}%(levelname)-8s{LogColors.RESET} | %(asctime)s | %(name)s | %(message)s",
        logging.INFO: f"{LogColors.INFO}%(levelname)-8s{LogColors.RESET} | %(asctime)s | %(name)s | %(message)s",
        logging.WARNING: f"{LogColors.WARNING}%(levelname)-8s{LogColors.RESET} | %(asctime)s | %(name)s | %(message)s",
        logging.ERROR: f"{LogColors.ERROR}%(levelname)-8s{LogColors.RESET} | %(asctime)s | %(name)s | %(message)s",
        logging.CRITICAL: f"{LogColors.CRITICAL}%(levelname)-8s{LogColors.RESET} | %(asctime)s | %(name)s | %(message)s",
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


class FileFormatter(logging.Formatter):
    """Custom formatter for file output without colors."""
    
    def __init__(self):
        super().__init__(
            fmt='%(levelname)-8s | %(asctime)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    console: bool = True
) -> None:
    """Setup logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to log file. If None, only console logging is used.
        console: Whether to enable console logging.
    """
    # Get root logger
    root_logger = logging.getLogger()
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(level)
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(ColoredFormatter())
        root_logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(FileFormatter())
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name.
    
    Args:
        name: Name of the logger (typically __name__ of the module).
        
    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)


# Initialize default logging configuration
def init_default_logging():
    """Initialize default logging configuration."""
    # Create logs directory
    logs_dir = Path("./logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = logs_dir / f"antigravity_{timestamp}.log"
    
    # Setup logging
    setup_logging(
        log_level="INFO",
        log_file=str(log_file),
        console=True
    )


# Auto-initialize on import
init_default_logging()
