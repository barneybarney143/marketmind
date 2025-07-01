from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import yfinance as yf


class DataDownloader:
    """Download and cache historical OHLCV data."""

    def __init__(self, cache_dir: Path | None = None) -> None:
        self.cache_dir = cache_dir or Path("data")
        self.cache_dir.mkdir(exist_ok=True)

    @staticmethod
    def _normalize(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        """Return a normalized OHLCV DataFrame with prefixed columns."""
        if isinstance(df.columns, pd.MultiIndex):
            df = df.droplevel(-1, axis=1)
        df.index = pd.to_datetime(df.index)
        df.index.name = "date"
        df = df.sort_index()

        df = df.rename(columns=lambda c: str(c).lower().replace(" ", "_"))

        required = ["open", "high", "low", "close", "adj_close", "volume"]
        for col in required:
            if col not in df.columns:
                df[col] = pd.NA
        df = df[required]
        return df.add_prefix(f"{ticker.lower()}_")

    def get_history(
        self, ticker: str | Iterable[str], start: str, end: str
    ) -> pd.DataFrame:
        """Return historical data for *ticker* between *start* and *end*."""

        tickers = [ticker] if isinstance(ticker, str) else list(ticker)

        dfs: list[pd.DataFrame] = []
        for t in tickers:
            cache_file = self.cache_dir / f"{t}-{start}-{end}.parquet"
            if cache_file.exists():
                df_t = pd.read_parquet(cache_file)
            else:
                df_t = yf.download(
                    t,
                    start=start,
                    end=end,
                    progress=False,
                    auto_adjust=False,
                )
                if df_t.empty:
                    raise ValueError(f"No data returned for ticker '{t}'")
                df_t = self._normalize(df_t, t)
                df_t.to_parquet(cache_file)
            dfs.append(df_t)

        combined = pd.concat(dfs, axis=1)
        combined.index.name = "date"
        combined = combined.sort_index()

        if len(tickers) == 1:
            prefix = f"{tickers[0].lower()}_"
            combined = combined.rename(columns=lambda c: c.removeprefix(prefix))

        return combined.loc[pd.Timestamp(start) : pd.Timestamp(end)]
