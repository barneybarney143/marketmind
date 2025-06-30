# MarketMind

This repository is a template for a modern Python project. It includes linting with [Ruff](https://docs.astral.sh/ruff/), type checking with [mypy](https://mypy-lang.org/), and testing with [pytest](https://docs.pytest.org/).

Use this setup as a starting point for new projects that require a light-weight but strict development workflow.

## Running the Scripts

Install the dependencies first:

```bash
pip install -r requirements-dev.txt
```

Run the helper scripts by pointing `PYTHONPATH` at the `src` directory.
Below are short examples demonstrating the two command line tools.

```bash
# Back-test the built in RSI strategy on SPY for a couple of weeks
PYTHONPATH=./src python scripts/backtest.py \
    --strategy rsi \
    --ticker SPY \
    --start 2020-01-01 \
    --end 2020-01-15 \
    --params '{"rsi_buy": 30, "rsi_sell": 70}'

# Show the latest signal from the RSI strategy
PYTHONPATH=./src python scripts/signal.py \
    --strategy rsi \
    --ticker SPY \
    --lookback 10
```

Each command prints either a summary table (for the back-test) or the latest
trading signal to standard output.
