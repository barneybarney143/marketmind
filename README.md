# MarketMind

This repository is a template for a modern Python project. It includes linting with [Ruff](https://docs.astral.sh/ruff/), type checking with [mypy](https://mypy-lang.org/), and testing with [pytest](https://docs.pytest.org/).
Code is formatted with [Black](https://black.readthedocs.io/) and these checks run automatically via [pre-commit](https://pre-commit.com/).

Use this setup as a starting point for new projects that require a light-weight but strict development workflow.

## Running the Scripts

## Setup

```bash
pip install poetry
poetry install --with dev
pre-commit install
```

Exporting requirements for Streamlit

```bash
make export
```

Run the helper scripts by pointing `PYTHONPATH` at the `src` directory:

```bash
PYTHONPATH=./src python scripts/backtest.py ...
PYTHONPATH=./src python scripts/signal.py ...
```

## Streamlit UI

Run the interactive web app locally:

```bash
# local
pip install -e .[dev] streamlit plotly
streamlit run streamlit_app.py
```
