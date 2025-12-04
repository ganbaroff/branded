"""
Unit tests for utility functions.
"""

import pytest
import logging
from branded.utils import setup_logger, validate_config, format_message


def test_setup_logger():
    """Test logger setup."""
    logger = setup_logger("test_logger", level="INFO")
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO


def test_setup_logger_with_custom_level():
    """Test logger setup with custom level."""
    logger = setup_logger("debug_logger", level="DEBUG")
    assert logger.level == logging.DEBUG


def test_validate_config_valid():
    """Test config validation with valid configuration."""
    config = {
        "agent": {
            "name": "TestAgent"
        },
        "settings": {
            "log_level": "INFO"
        }
    }
    
    required_keys = ["agent.name", "settings.log_level"]
    assert validate_config(config, required_keys) is True


def test_validate_config_missing_key():
    """Test config validation with missing key."""
    config = {
        "agent": {
            "name": "TestAgent"
        }
    }
    
    required_keys = ["agent.name", "settings.log_level"]
    assert validate_config(config, required_keys) is False


def test_format_message_short():
    """Test message formatting with short message."""
    message = "Short message"
    formatted = format_message(message, max_length=100)
    assert formatted == message


def test_format_message_long():
    """Test message formatting with long message."""
    message = "A" * 150
    formatted = format_message(message, max_length=100)
    assert len(formatted) == 100
    assert formatted.endswith("...")


def test_format_message_exact_length():
    """Test message formatting with exact length."""
    message = "A" * 100
    formatted = format_message(message, max_length=100)
    assert formatted == message
    assert not formatted.endswith("...")
