# signal.py

Utility script to show the latest trading signal produced by a strategy.
It downloads recent price history via `DataDownloader` and feeds it to the chosen
strategy's `next_bar` method.

Run for a single strategy or all available ones:

```bash
PYTHONPATH=./src python signal.py --strategy rsi --ticker AAPL
PYTHONPATH=./src python signal.py --all --ticker AAPL
```

### Arguments
- `--strategy` – name of a strategy to run
- `--all` – run every strategy defined in `strategies`
- `--ticker` – ticker symbol to evaluate
- `--lookback` – number of days of history to download
