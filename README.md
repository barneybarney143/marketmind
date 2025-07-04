# MarketMind

This repository provides a minimal Python project using modern tooling. It ships with a small example package and is ready for development with type checking, linting, testing and pre-commit hooks.

Documentation from the previous project is kept in the `docs/` directory for reference.

## Installation

Use [Poetry](https://python-poetry.org/) to manage dependencies:

```bash
pip install poetry
poetry install --with dev
```

Activate pre-commit hooks after installing:

```bash
poetry run pre-commit install
```

## Usage

Call the example function from Python:

```python
from my_package import say_hello
print(say_hello())
```

## Development

Run the quality checks and tests locally before committing:

```bash
poetry run ruff .
poetry run mypy src
poetry run pytest
```

## Contributing

Pull requests are welcome. Enable branch protection on `main` to require passing status checks before merge.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
