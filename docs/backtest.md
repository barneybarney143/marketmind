# backtest.py

Command line script to run back-tests for the trading strategies defined in `src/strategies`.
It downloads historical data with `DataDownloader`, feeds each bar into a `Backtester`
instance and prints a performance summary. Parameters may be supplied as JSON and
expanded into a grid when `--sweep` is used.

## Usage

```bash
PYTHONPATH=./src python backtest.py --strategy rsi --ticker AAPL --start 2020-01-01 --end 2021-01-01 --params '{"rsi_buy": 30, "rsi_sell": 70}'
```

### Arguments
- `--strategy` – name of a strategy to run (exclusive with `--all`)
- `--all` – run all available strategies
- `--ticker` – ticker symbol to back-test
- `--start`/`--end` – ISO date range for the test
- `--params` – JSON string of strategy parameters
- `--sweep` – run all combinations of the parameter grid

Results are written to `results/` with the parameter hash in the filename.
