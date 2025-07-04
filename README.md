# MarketMind

This repository is a template for a modern Python project. It includes linting with [Ruff](https://docs.astral.sh/ruff/), type checking with [mypy](https://mypy-lang.org/), and testing with [pytest](https://docs.pytest.org/).
Code is formatted with [Black](https://black.readthedocs.io/) and these checks run automatically via [pre-commit](https://pre-commit.com/).

Use this setup as a starting point for new projects that require a light-weight but strict development workflow.
See the [Class Intent Reference](docs/class_intent.md) for a summary of all
classes and their roles in the current code base.

## Running the Scripts

Install the dependencies first:

```bash
pip install -e .[dev]
```

Set up the pre-commit hooks after installing the requirements:

```bash
pre-commit install
```

Run the helper scripts by pointing `PYTHONPATH` at the `src` directory:

```bash
PYTHONPATH=./src python backtest.py ...
PYTHONPATH=./src python signal.py ...
```

For example, run a simple back-test of the RSI strategy on AAPL:

```bash
PYTHONPATH=./src python backtest.py \
  --strategy rsi --ticker AAPL --start 2020-01-01 --end 2021-01-01 \
  --params '{"rsi_buy": 30, "rsi_sell": 70}'
```

To sweep parameter combinations, pass lists in `--params` and add `--sweep`:

```bash
PYTHONPATH=./src python backtest.py \
  --strategy rsi --ticker AAPL --start 2020-01-01 --end 2021-01-01 \
  --params '{"rsi_buy": [20, 30], "rsi_sell": [70, 80]}' --sweep
```

You can print the most recent signal for a ticker with:

```bash
PYTHONPATH=./src python signal.py \
  --strategy rsi --ticker AAPL --lookback 365
```
To check the latest signal from every strategy:
```bash
PYTHONPATH=./src python signal.py \
  --all --ticker AAPL --lookback 365
```

## Streamlit UI

Run the interactive web app locally:

```bash
pip install -e .[streamlit]
streamlit run streamlit_app.py
```

## Quick data pull

Fetch price history from the command line:

```bash
python fetch.py --tickers "SPY,IDTL" --start 2020-01-01 --end 2020-01-10 \
  --csv-out data
```

## Checking code quality

Before committing, run the linters, type checker, and tests:

```bash
ruff check .
mypy
pytest -q
```

## EU-friendly Reddit strategies

The following UCITS ETFs are used to replicate popular leveraged Reddit portfolios in the EEA.

| US Ticker | UCITS Ticker |
|-----------|--------------|
| UPRO | 3USL |
| TMF  | 3TYL |
| TQQQ | QQQ3 |
| SPY  | CSPX |
| TLT  | IDTL |
