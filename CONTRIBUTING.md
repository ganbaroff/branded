# Contributing to Branded

Thank you for your interest in contributing to Branded! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/branded.git
   cd branded
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines

3. Add tests for any new functionality

4. Run the test suite:
   ```bash
   pytest tests/ -v
   ```

5. Ensure your code passes linting:
   ```bash
   black src/
   flake8 src/
   ```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public classes and methods
- Keep functions focused and modular
- Use meaningful variable names

### Testing

- Write unit tests for new features
- Ensure all tests pass before submitting a PR
- Aim for high test coverage
- Use descriptive test names that explain what is being tested

### Documentation

- Update documentation for any API changes
- Add docstrings to new classes and methods
- Update the README if adding new features
- Add examples if appropriate

## Submitting Changes

1. Commit your changes with a clear message:
   ```bash
   git commit -m "Add feature: description of changes"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Open a Pull Request on GitHub with:
   - Clear description of the changes
   - Reference to any related issues
   - Screenshots if applicable (for UI changes)

## Pull Request Guidelines

- Keep PRs focused on a single feature or bugfix
- Write clear PR descriptions
- Update documentation as needed
- Ensure all tests pass
- Respond to review feedback promptly
- Keep commits clean and meaningful

## Code Review Process

1. A maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR

## Reporting Bugs

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Any relevant logs or error messages

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Provide a clear description of the feature
- Explain the use case and benefits
- Be open to discussion about implementation

## Questions?

If you have questions, feel free to:

- Open an issue on GitHub
- Reach out to the maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

Thank you for contributing to Branded!
