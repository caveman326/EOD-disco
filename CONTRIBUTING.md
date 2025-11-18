# Contributing to EOD Stock Scans

Thank you for your interest in contributing to EOD Stock Scans! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/eodstockscans.git
cd eodstockscans
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Comment complex logic

## Adding New Scans

When adding new scan strategies:

1. Add the scan definition to `src/scans.py`
2. Include proper attribution to the original strategy creator
3. Document the scan criteria clearly
4. Test the scan with sample data

## Submitting Changes

1. Ensure your code follows the style guidelines
2. Test your changes thoroughly
3. Update documentation if necessary
4. Write clear commit messages
5. Submit a pull request with a description of your changes

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- System information (OS, Python version, etc.)

## Feature Requests

Feature requests are welcome! Please:

- Check if the feature has already been requested
- Provide a clear description of the feature
- Explain the use case and benefits
- Be open to discussion and feedback

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing opinions and experiences

## Questions?

If you have questions, feel free to:

- Open an issue for discussion
- Reach out to the maintainers
- Check existing documentation

Thank you for contributing!
