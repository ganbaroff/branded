"""
Configuration management for the Branded AI framework.
"""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class Config:
    """
    Configuration manager for agents.
    
    Supports loading from YAML files and environment variables.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self._config: Dict[str, Any] = {}
        
        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)
        else:
            self._load_defaults()
    
    def _load_defaults(self) -> None:
        """Load default configuration values."""
        self._config = {
            "agent": {
                "name": "BrandedAgent",
                "version": "0.1.0",
                "description": "AI Agent powered by Branded framework"
            },
            "settings": {
                "log_level": "INFO",
                "max_retries": 3,
                "timeout": 30
            }
        }
    
    def load_from_file(self, config_path: str) -> None:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        try:
            with open(config_path, 'r') as f:
                loaded_config = yaml.safe_load(f)
                if loaded_config:
                    self._config.update(loaded_config)
        except Exception as e:
            raise ValueError(f"Failed to load configuration from {config_path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key (supports dot notation).
        
        Args:
            key: Configuration key (e.g., 'agent.name' or 'settings.log_level')
            default: Default value if key not found
            
        Returns:
            The configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value by key (supports dot notation).
        
        Args:
            key: Configuration key (e.g., 'agent.name')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.
        
        Returns:
            Dictionary containing all configuration
        """
        return self._config.copy()
    
    def save_to_file(self, config_path: str) -> None:
        """
        Save configuration to a YAML file.
        
        Args:
            config_path: Path where to save the configuration
        """
        try:
            Path(config_path).parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                yaml.dump(self._config, f, default_flow_style=False)
        except Exception as e:
            raise ValueError(f"Failed to save configuration to {config_path}: {e}")
