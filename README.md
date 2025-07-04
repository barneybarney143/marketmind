# MarketMind

This repository contains a minimal hello world example. The project demonstrates a basic development workflow using **Ruff**, **mypy**, and **pytest**.

## Setup

Install the development dependencies:

```bash
pip install -e .[dev]
```

## Running checks

Run the linters, type checker and tests:

```bash
ruff check .
mypy
pytest -q
```
