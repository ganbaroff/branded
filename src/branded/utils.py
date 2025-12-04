"""
Utility functions for the Branded AI framework.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with the specified configuration.
    
    Args:
        name: Name of the logger
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def validate_config(config_dict: dict, required_keys: list) -> bool:
    """
    Validate that a configuration dictionary contains all required keys.
    
    Args:
        config_dict: Configuration dictionary to validate
        required_keys: List of required keys (supports dot notation)
        
    Returns:
        True if all required keys are present, False otherwise
    """
    for key in required_keys:
        keys = key.split('.')
        value = config_dict
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
    
    return True


def format_message(message: str, max_length: int = 100) -> str:
    """
    Format a message to fit within a maximum length.
    
    Args:
        message: Message to format
        max_length: Maximum length of the formatted message
        
    Returns:
        Formatted message
    """
    if len(message) <= max_length:
        return message
    
    return message[:max_length - 3] + "..."
