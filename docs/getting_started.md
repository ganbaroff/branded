# Getting Started with Branded

This guide will help you get started with the Branded AI agent framework.

## Installation

### From Source

```bash
git clone https://github.com/ganbaroff/branded.git
cd branded
pip install -e .
```

### Using pip (once published)

```bash
pip install branded
```

## Your First Agent

Create a simple agent in just a few lines:

```python
from branded import Agent

# Create an agent
agent = Agent(name="MyFirstAgent")

# Run it
agent.run()
```

## Creating Custom Agents

Extend the base `Agent` class to create custom behavior:

```python
from branded import Agent

class MyCustomAgent(Agent):
    def _execute(self):
        """Override this method with your custom logic."""
        self.logger.info("My custom agent is running!")
        
        # Do your custom work here
        self.set_state("status", "completed")

# Use your custom agent
agent = MyCustomAgent(name="CustomAgent")
agent.run()
```

## Using Configuration

Create a `config.yaml` file:

```yaml
agent:
  name: "MyConfiguredAgent"
  version: "1.0.0"

settings:
  log_level: "DEBUG"
  max_retries: 5
```

Load and use it:

```python
from branded import Agent, Config

config = Config(config_path="config.yaml")
agent = Agent(
    name=config.get("agent.name"),
    config=config,
    log_level=config.get("settings.log_level")
)
agent.run()
```

## Managing Agent State

Agents can maintain state during execution:

```python
agent = Agent(name="StatefulAgent")

# Set state
agent.set_state("counter", 0)
agent.set_state("data", {"key": "value"})

# Get state
counter = agent.get_state("counter")
data = agent.get_state("data")

# Clear state
agent.clear_state()
```

## Logging

Agents come with built-in logging:

```python
from branded import Agent

# Set log level when creating agent
agent = Agent(name="MyAgent", log_level="DEBUG")

# Logs are automatically created for agent lifecycle events
agent.run()
```

## Next Steps

- Check out the `examples/` directory for more examples
- Read the API documentation in `docs/`
- Build your own custom agents!

## Common Patterns

### Long-Running Agent

```python
import time

class LongRunningAgent(Agent):
    def _execute(self):
        while self._running:
            self.logger.info("Working...")
            # Do some work
            time.sleep(1)
```

### Agent with Error Handling

```python
class RobustAgent(Agent):
    def _execute(self):
        try:
            # Your agent logic
            self.logger.info("Executing task...")
        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            # Handle error appropriately
```

## Troubleshooting

### Import Errors

Make sure you've installed the package:
```bash
pip install -e .
```

### Configuration Not Loading

Check that your YAML file path is correct and the file is valid YAML syntax.

### Logging Not Appearing

Ensure you've set an appropriate log level:
```python
agent = Agent(log_level="DEBUG")  # or "INFO", "WARNING", etc.
```
