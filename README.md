# Branded - AI Agent Framework

A flexible and extensible AI agent framework for building intelligent automation and conversation agents.

## Features

- 🤖 Modular agent architecture
- 🔧 Easy configuration and customization
- 📝 Built-in logging and monitoring
- 🔌 Extensible plugin system
- 🚀 Simple deployment

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ganbaroff/branded.git
cd branded

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from branded import Agent

# Create a simple agent
agent = Agent(name="MyAgent")

# Run the agent
agent.run()
```

## Project Structure

```
branded/
├── src/
│   └── branded/          # Main package
│       ├── __init__.py
│       ├── agent.py      # Core agent class
│       ├── config.py     # Configuration management
│       └── utils.py      # Utility functions
├── examples/             # Example agents
├── tests/               # Test suite
├── docs/                # Documentation
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Configuration

Create a `config.yaml` file in your project directory:

```yaml
agent:
  name: "MyAgent"
  version: "1.0.0"
  description: "A custom AI agent"

settings:
  log_level: "INFO"
  max_retries: 3
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. Format your code with:

```bash
black src/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Contact

For questions and support, please open an issue on GitHub.