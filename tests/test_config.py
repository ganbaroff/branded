"""
Unit tests for the Config class.
"""

import pytest
import os
import tempfile
from branded import Config


def test_config_creation_with_defaults():
    """Test that config is created with default values."""
    config = Config()
    
    assert config.get("agent.name") == "BrandedAgent"
    assert config.get("settings.log_level") == "INFO"
    assert config.get("settings.max_retries") == 3


def test_config_get_with_default():
    """Test getting config values with default fallback."""
    config = Config()
    
    # Non-existent key should return default
    assert config.get("nonexistent.key", "default_value") == "default_value"


def test_config_set():
    """Test setting config values."""
    config = Config()
    
    config.set("custom.key", "custom_value")
    assert config.get("custom.key") == "custom_value"
    
    # Test nested setting
    config.set("nested.deep.key", 42)
    assert config.get("nested.deep.key") == 42


def test_config_to_dict():
    """Test converting config to dictionary."""
    config = Config()
    config.set("test.key", "test_value")
    
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert "test" in config_dict
    assert config_dict["test"]["key"] == "test_value"


def test_config_load_from_file():
    """Test loading config from a YAML file."""
    # Create a temporary YAML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
agent:
  name: "TestAgent"
  version: "2.0.0"

settings:
  log_level: "DEBUG"
  custom_setting: "test_value"
""")
        temp_path = f.name
    
    try:
        config = Config(config_path=temp_path)
        
        assert config.get("agent.name") == "TestAgent"
        assert config.get("agent.version") == "2.0.0"
        assert config.get("settings.log_level") == "DEBUG"
        assert config.get("settings.custom_setting") == "test_value"
    finally:
        os.unlink(temp_path)


def test_config_save_to_file():
    """Test saving config to a YAML file."""
    config = Config()
    config.set("test.key", "test_value")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_path = f.name
    
    try:
        config.save_to_file(temp_path)
        
        # Load the saved config
        new_config = Config(config_path=temp_path)
        assert new_config.get("test.key") == "test_value"
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_config_invalid_file_path():
    """Test that invalid file path raises error."""
    config = Config()
    
    with pytest.raises(ValueError):
        config.load_from_file("/nonexistent/path/config.yaml")
