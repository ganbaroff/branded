"""
Unit tests for the Agent class.
"""

import pytest
from branded import Agent


def test_agent_creation():
    """Test that an agent can be created with default parameters."""
    agent = Agent()
    assert agent.name == "BrandedAgent"
    assert not agent.is_running()


def test_agent_with_custom_name():
    """Test that an agent can be created with a custom name."""
    agent = Agent(name="TestAgent")
    assert agent.name == "TestAgent"


def test_agent_state_management():
    """Test getting and setting agent state."""
    agent = Agent()
    
    # Test setting state
    agent.set_state("key1", "value1")
    assert agent.get_state("key1") == "value1"
    
    # Test getting non-existent key
    assert agent.get_state("nonexistent") is None
    
    # Test clearing state
    agent.clear_state()
    assert agent.get_state("key1") is None


def test_agent_run():
    """Test that an agent can run without errors."""
    agent = Agent(name="TestAgent")
    
    # Should run without raising an exception
    agent.run()
    
    # Agent should not be running after completion
    assert not agent.is_running()


def test_agent_repr():
    """Test the string representation of an agent."""
    agent = Agent(name="TestAgent")
    repr_str = repr(agent)
    assert "TestAgent" in repr_str
    assert "running=False" in repr_str


class CustomTestAgent(Agent):
    """A custom agent for testing override behavior."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executed = False
    
    def _execute(self):
        self.executed = True
        self.set_state("custom_state", "executed")


def test_custom_agent_execution():
    """Test that custom agent execution works correctly."""
    agent = CustomTestAgent(name="CustomTest")
    
    assert not agent.executed
    agent.run()
    assert agent.executed
    assert agent.get_state("custom_state") == "executed"
