from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf


class DataDownloader:
    """Download and cache historical OHLCV data."""

    def __init__(self, cache_dir: Path | None = None) -> None:
        self.cache_dir = cache_dir or Path("data")
        self.cache_dir.mkdir(exist_ok=True)

    def get_history(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """Return historical data for *ticker* between *start* and *end*.

        Parameters
        ----------
        ticker:
            Ticker symbol understood by yfinance.
        start:
            Inclusive start date in ``YYYY-MM-DD`` format.
        end:
            Exclusive end date in ``YYYY-MM-DD`` format.
        """
        cache_file = self.cache_dir / f"{ticker}.parquet"
        if cache_file.exists():
            df = pd.read_parquet(cache_file)
        else:
            df = yf.download(
                ticker, start=start, end=end, progress=False, auto_adjust=False
            )
            if df.empty:
                raise ValueError(f"No data returned for ticker '{ticker}'")
            df.to_parquet(cache_file)
        df.index.name = "date"
        df = df.loc[pd.Timestamp(start) : pd.Timestamp(end)]
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns = pd.Index([str(c).lower() for c in df.columns])
        return df
