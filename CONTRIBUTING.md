# Contributing to Small-Diff

Thank you for your interest in contributing to Small-Diff! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

## Getting Started

1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/small-diff.git
   cd small-diff
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/original-owner/small-diff.git
   ```

## Development Setup

### Prerequisites

- Python 3.x (we recommend using `pyenv` to manage Python versions)
- `pipenv` for virtual environment and dependency management
- `make` (for using the provided Makefile commands)

### Python Version Management

We recommend using `pyenv` to manage your Python versions. This ensures consistency across different development environments.

1. **Install pyenv** (if not already installed):
   - **macOS**: `brew install pyenv`
   - **Linux**: Follow the [official pyenv installation guide](https://github.com/pyenv/pyenv#installation)
   - **Windows**: Use `pyenv-win` or WSL

2. **Install the required Python version**:
   ```bash
   pyenv install 3.8.0  # or the version specified in the project
   pyenv local 3.8.0    # set the local version for this project
   ```

### Installing pipenv

Install `pipenv` for virtual environment and dependency management:
```bash
pip install pipenv
```

### Project Installation

#### Mac/Linux

The easiest way to set up the development environment is using the provided Makefile:
```bash
make install
```

This command will:
- Create a new virtual environment
- Install all dependencies listed in `Pipfile.lock`
- Set up the development environment

#### Windows

On Windows, you'll need to install GNU Make first:
1. Download GNU Make from the [official website](http://gnuwin32.sourceforge.net/packages/make.htm)
2. Install it and add it to your PATH
3. Navigate to the project directory and run:
   ```bash
   make install
   ```

#### Manual Installation (Alternative)

If you prefer to install manually:
```bash
# Install the project in development mode
pipenv install --dev

# Activate the virtual environment
pipenv shell
```

### Running Tests

```bash
# Using the provided test script
./scripts/test.sh

# Or using make
make test

# Or directly with pytest
pytest

# Run with coverage
pytest --cov=smalldiff
```

## Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add minimal, standard docstrings to all public functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Code Formatting

We recommend using:
- `black` for code formatting
- `flake8` for linting
- `isort` for import sorting

You can format your code before committing:
```bash
black smalldiff/ tests/
isort smalldiff/ tests/
```

## Testing

### Writing Tests

- Write tests for all new functionality
- Follow the existing test structure in the `tests/` directory
- Use descriptive test names
- Aim for good test coverage
- Use pytest fixtures when appropriate

### Test Structure

- Unit tests should be in `tests/`
- Test files should be named `test_*.py`
- Test functions should be named `test_*`

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, focused commits
   - Use conventional commit messages
   - Keep commits atomic and logical

3. **Test your changes**:
   ```bash
   ./scripts/test.sh
   ```

4. **Update documentation**:
   - Update README.md if needed
   - Add docstrings for new functions
   - Update any relevant documentation

5. **Submit your PR**:
   - Provide a clear description of changes
   - Reference any related issues
   - Include test results if applicable

### Commit Message Format

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(encoder): add new encoding method`
- `fix(main): resolve memory leak in diff calculation`
- `docs(readme): update installation instructions`

## Issue Reporting

### Before Submitting an Issue

1. Check existing issues to avoid duplicates
2. Search the documentation for solutions
3. Try to reproduce the issue with the latest version

### Issue Template

When reporting issues, please include:

- **Description**: Clear description of the problem
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, Python version, package versions
- **Additional context**: Any other relevant information

## Code of Conduct

### Our Standards

- We encourage being respectful and inclusive of all contributors
- Please use welcoming and inclusive language in all interactions
- Let's collaborate constructively to achieve our shared goals
- Together we can focus on what benefits the whole community
- We appreciate showing empathy and understanding towards each other

### Enforcement

- We aim to maintain a welcoming environment for all contributors
- Repeated violations of our standards may result in temporary restrictions 
- Project maintainers will work with contributors to resolve any concerns, and suggest improvements to these guidelines through pull requests

## Getting Help

- Check the [README.md](README.md) for basic information
- Search existing issues for similar problems
- Open a new issue for bugs or feature requests
- Join our community discussions (if available)

## License

By contributing to Small-Diff, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Small-Diff! Your contributions help make this project better for everyone. 