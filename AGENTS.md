# Coding and Testing Standards

This project follows strict linting and typing rules. The main tools are:

- **Ruff** for linting (configured in `pyproject.toml`)
- **mypy** for static type checking
- **pytest** for testing

All code must pass Ruff, mypy, and pytest locally before being committed. Continuous integration runs these tools on every push and pull request to `main`.
