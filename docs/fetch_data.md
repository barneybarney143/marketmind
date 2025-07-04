# fetch_data.py

Lightweight helper around `DataDownloader` providing a `fetch()` function.
It accepts one or more ticker symbols and returns a dictionary of
`pandas.DataFrame` objects with OHLCV data.

When run as `python -m fetch_data TICKER ...` it writes the data to CSV files in
the current directory.

```python
from fetch_data import fetch
prices = fetch(["SPY", "AAPL"], start="2020-01-01", end="2020-12-31")
```

### Parameters
- `tickers` – single symbol or iterable of symbols
- `start` / `end` – ISO date range
- `interval` – bar interval (currently unused)
- `ucits_map` – map US tickers to UCITS equivalents when `True`
