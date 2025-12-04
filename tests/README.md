# Branded Tests

This directory contains the test suite for the Branded AI agent framework.

## Running Tests

To run all tests:

```bash
pytest tests/
```

To run tests with coverage:

```bash
pytest --cov=branded --cov-report=html tests/
```

To run a specific test file:

```bash
pytest tests/test_agent.py
```

## Test Structure

- `test_agent.py` - Tests for the core Agent class
- `test_config.py` - Tests for configuration management
- `test_utils.py` - Tests for utility functions
