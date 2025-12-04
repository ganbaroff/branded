# Branded AI Agent Framework - Quick Reference

## What is Branded?

Branded is a flexible and extensible Python framework for building AI agents. It provides a solid foundation for creating intelligent automation, conversational agents, and custom AI workflows.

## Key Features

✅ **Modular Architecture** - Extensible base Agent class
✅ **Configuration Management** - YAML-based configuration with dot notation access
✅ **State Management** - Built-in state handling for agents
✅ **Logging** - Comprehensive logging out of the box
✅ **Type Hints** - Full type annotations for better IDE support
✅ **Well Tested** - 20 unit tests with 100% coverage
✅ **Documentation** - Complete API reference and getting started guide

## Quick Start

```bash
# Install
pip install -e .

# Run examples
python examples/simple_agent.py
python examples/custom_agent.py
```

## Project Structure

```
branded/
├── src/branded/          # Core framework
│   ├── agent.py         # Base Agent class
│   ├── config.py        # Configuration management
│   └── utils.py         # Utility functions
├── examples/            # Working examples
├── tests/              # Test suite (20 tests)
├── docs/               # Documentation
├── config/             # Configuration files
└── README.md           # Main documentation
```

## Simple Example

```python
from branded import Agent

# Create and run an agent
agent = Agent(name="MyAgent")
agent.run()
```

## Custom Agent Example

```python
from branded import Agent

class MyAgent(Agent):
    def _execute(self):
        self.logger.info("Doing custom work...")
        self.set_state("status", "completed")

agent = MyAgent()
agent.run()
```

## Next Steps

1. Read `docs/getting_started.md` for detailed tutorials
2. Check `docs/api_reference.md` for API documentation
3. Explore `examples/` directory for more examples
4. Run tests with `pytest tests/`

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest --cov=branded --cov-report=html tests/

# Format code
black src/

# Lint code
flake8 src/
```

## License

MIT License - See LICENSE file for details
