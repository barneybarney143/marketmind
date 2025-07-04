# data.py

Implements `DataDownloader`, a simple wrapper around the `yfinance` library.
It caches downloaded OHLCV data as parquet files under `data/` to avoid
repeated network requests. Columns are normalised to lowercase names and ticker
prefixes.

```python
from data import DataDownloader
loader = DataDownloader()
df = loader.get_history("SPY", "2020-01-01", "2020-12-31")
```

The `ticker_map` dictionary defines UCITS equivalents for some common US ETFs.
