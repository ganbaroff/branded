# API Reference

## Core Classes

### Agent

The base class for all agents in the Branded framework.

#### Constructor

```python
Agent(name="BrandedAgent", config=None, log_level="INFO")
```

**Parameters:**
- `name` (str): The name of the agent
- `config` (Config, optional): Configuration object
- `log_level` (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

#### Methods

##### run()

Start the agent's main execution loop.

```python
agent.run()
```

##### stop()

Stop the agent's execution.

```python
agent.stop()
```

##### is_running()

Check if the agent is currently running.

```python
if agent.is_running():
    print("Agent is running")
```

**Returns:** `bool`

##### get_state(key)

Get a value from the agent's state.

```python
value = agent.get_state("key")
```

**Parameters:**
- `key` (str): The state key to retrieve

**Returns:** The value associated with the key, or `None`

##### set_state(key, value)

Set a value in the agent's state.

```python
agent.set_state("key", "value")
```

**Parameters:**
- `key` (str): The state key to set
- `value` (Any): The value to store

##### clear_state()

Clear all state data.

```python
agent.clear_state()
```

##### _execute()

Main execution logic. Override this method in subclasses to implement custom behavior.

```python
class MyAgent(Agent):
    def _execute(self):
        # Your custom logic here
        pass
```

---

### Config

Configuration manager for agents.

#### Constructor

```python
Config(config_path=None)
```

**Parameters:**
- `config_path` (str, optional): Path to YAML configuration file

#### Methods

##### get(key, default=None)

Get a configuration value by key (supports dot notation).

```python
value = config.get("agent.name", "DefaultAgent")
```

**Parameters:**
- `key` (str): Configuration key (e.g., 'agent.name')
- `default` (Any): Default value if key not found

**Returns:** The configuration value or default

##### set(key, value)

Set a configuration value by key (supports dot notation).

```python
config.set("agent.name", "MyAgent")
```

**Parameters:**
- `key` (str): Configuration key
- `value` (Any): Value to set

##### to_dict()

Get the entire configuration as a dictionary.

```python
config_dict = config.to_dict()
```

**Returns:** `dict`

##### load_from_file(config_path)

Load configuration from a YAML file.

```python
config.load_from_file("config.yaml")
```

**Parameters:**
- `config_path` (str): Path to the YAML configuration file

##### save_to_file(config_path)

Save configuration to a YAML file.

```python
config.save_to_file("config.yaml")
```

**Parameters:**
- `config_path` (str): Path where to save the configuration

---

## Utility Functions

### setup_logger(name, level="INFO", log_file=None)

Set up a logger with the specified configuration.

```python
from branded.utils import setup_logger

logger = setup_logger("my_logger", level="DEBUG")
```

**Parameters:**
- `name` (str): Name of the logger
- `level` (str): Logging level
- `log_file` (str, optional): Path to log file

**Returns:** `logging.Logger`

### validate_config(config_dict, required_keys)

Validate that a configuration dictionary contains all required keys.

```python
from branded.utils import validate_config

is_valid = validate_config(config_dict, ["agent.name", "settings.log_level"])
```

**Parameters:**
- `config_dict` (dict): Configuration dictionary to validate
- `required_keys` (list): List of required keys (supports dot notation)

**Returns:** `bool`

### format_message(message, max_length=100)

Format a message to fit within a maximum length.

```python
from branded.utils import format_message

formatted = format_message("Very long message...", max_length=50)
```

**Parameters:**
- `message` (str): Message to format
- `max_length` (int): Maximum length of the formatted message

**Returns:** `str`

---

## Configuration Schema

Default configuration structure:

```yaml
agent:
  name: "BrandedAgent"
  version: "0.1.0"
  description: "AI Agent powered by Branded framework"

settings:
  log_level: "INFO"
  max_retries: 3
  timeout: 30
```

You can extend this with your own custom fields.
