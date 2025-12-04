"""
Core Agent class for the Branded AI framework.
"""

import logging
from typing import Optional, Dict, Any
from .config import Config
from .utils import setup_logger


class Agent:
    """
    Base Agent class that provides core functionality for AI agents.
    
    Attributes:
        name (str): The name of the agent
        config (Config): Configuration object for the agent
        logger (logging.Logger): Logger instance for the agent
    """
    
    def __init__(
        self,
        name: str = "BrandedAgent",
        config: Optional[Config] = None,
        log_level: str = "INFO"
    ):
        """
        Initialize a new Agent instance.
        
        Args:
            name: The name of the agent
            config: Optional configuration object
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.name = name
        self.config = config or Config()
        self.logger = setup_logger(name, log_level)
        self._state: Dict[str, Any] = {}
        self._running = False
        
        self.logger.info(f"Agent '{self.name}' initialized")
    
    def run(self) -> None:
        """
        Start the agent's main execution loop.
        """
        self.logger.info(f"Starting agent '{self.name}'")
        self._running = True
        
        try:
            self._execute()
        except Exception as e:
            self.logger.error(f"Error during agent execution: {e}", exc_info=True)
            raise
        finally:
            self._running = False
            self.logger.info(f"Agent '{self.name}' stopped")
    
    def _execute(self) -> None:
        """
        Main execution logic. Override this method in subclasses.
        """
        self.logger.info("Agent is running... (Override _execute method for custom behavior)")
    
    def stop(self) -> None:
        """
        Stop the agent's execution.
        """
        self.logger.info(f"Stopping agent '{self.name}'")
        self._running = False
    
    def is_running(self) -> bool:
        """
        Check if the agent is currently running.
        
        Returns:
            bool: True if agent is running, False otherwise
        """
        return self._running
    
    def get_state(self, key: str) -> Any:
        """
        Get a value from the agent's state.
        
        Args:
            key: The state key to retrieve
            
        Returns:
            The value associated with the key, or None if not found
        """
        return self._state.get(key)
    
    def set_state(self, key: str, value: Any) -> None:
        """
        Set a value in the agent's state.
        
        Args:
            key: The state key to set
            value: The value to store
        """
        self._state[key] = value
        self.logger.debug(f"State updated: {key} = {value}")
    
    def clear_state(self) -> None:
        """
        Clear all state data.
        """
        self._state.clear()
        self.logger.debug("Agent state cleared")
    
    def __repr__(self) -> str:
        return f"Agent(name='{self.name}', running={self._running})"
