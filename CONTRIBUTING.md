# CONTRIBUTING.md

## Contributing to NHP Claims Assessor

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Install dev dependencies: `pip install -e ".[dev]"`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write/update tests: `pytest tests/ -v`
4. Format code: `black src/ tests/`
5. Check linting: `flake8 src/ tests/`
6. Type checking: `mypy src/`
7. Commit with meaningful message: `git commit -m "Add feature: description"`
8. Push to your fork and open a Pull Request

## Testing

- Write tests for new features
- Ensure all tests pass: `pytest tests/ -v --cov=src`
- Maintain >80% code coverage

## Code Style

- Follow PEP 8
- Use Black for formatting
- Use type hints
- Write docstrings for modules, classes, and functions

## Commit Messages

- Use clear, descriptive messages
- Start with verb: "Add", "Fix", "Update", "Refactor"
- Reference issues when applicable: "Fixes #123"

## Pull Requests

- Provide clear description of changes
- Link related issues
- Ensure CI/CD passes
- Address review feedback

## Issues

- Check existing issues before opening new ones
- Provide clear reproduction steps for bugs
- Include expected vs actual behavior

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new code
- Update CHANGELOG.md

Thank you for contributing!
