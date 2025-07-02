from __future__ import annotations

from pathlib import Path
from typing import Iterable
import re

import pandas as pd
import yfinance as yf

# Map of US tickers to their UCITS equivalents
ticker_map = {
    "UPRO": "3USL",
    "TMF": "3TYL",
    "TQQQ": "QQQ3",
    "SPY": "CSPX",
    "TLT": "IDTL",
}


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

        if isinstance(ticker, str):
            tickers = [t.strip() for t in re.split(r"[,\s]+", ticker) if t.strip()]
        else:
            tickers = list(ticker)

        remote_map = {t: ticker_map.get(t, t) for t in tickers}

        dfs: list[pd.DataFrame] = []
        for orig, remote in remote_map.items():
            cache_file = self.cache_dir / f"{orig}-{start}-{end}.parquet"
            if cache_file.exists():
                df_t = pd.read_parquet(cache_file)
            else:
                df_t = yf.download(
                    remote,
                    start=start,
                    end=end,
                    progress=False,
                    auto_adjust=False,
                )
                if df_t.empty:
                    raise ValueError(f"No data returned for ticker '{remote}'")
                df_t = self._normalize(df_t, orig)
                df_t.to_parquet(cache_file)
            dfs.append(df_t)

        combined = pd.concat(dfs, axis=1)
        combined.index.name = "date"
        combined = combined.sort_index()

        if len(tickers) == 1:
            prefix = f"{tickers[0].lower()}_"
            combined = combined.rename(columns=lambda c: c.removeprefix(prefix))

        return combined.loc[pd.Timestamp(start) : pd.Timestamp(end)]
