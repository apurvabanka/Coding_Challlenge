import logging
from datetime import datetime


def setup_logger(log_file: str = "deduplication.log") -> logging.Logger:
    """
    Setup a simple logger with date/time and file output
    
    Args:
        log_file: Path to the log file
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger("deduplication_logger")
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Format with timestamp
    formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def log_change(action: str, value_from: str = None, value_to: str = None, additional_info: str = ""):
    """
    Log a change with from/to values and timestamp
    
    Args:
        action: Description of the action being performed
        value_from: The original value (optional)
        value_to: The new value (optional)
        additional_info: Any additional information to include
    """
    logger = logging.getLogger("deduplication_logger")
    
    # Build the log message
    message_parts = [action]
    
    if value_from is not None and value_to is not None:
        message_parts.append(f"from '{value_from}' to '{value_to}'")
    elif value_from is not None:
        message_parts.append(f"from '{value_from}'")
    elif value_to is not None:
        message_parts.append(f"to '{value_to}'")
    
    if additional_info:
        message_parts.append(f"({additional_info})")
    
    message = " ".join(message_parts)
    logger.info(message)


def log_info(message: str):
    """Log a simple info message with timestamp"""
    logger = logging.getLogger("deduplication_logger")
    logger.info(message)

