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

    def get_history(
        self, ticker: str | Iterable[str], start: str, end: str
    ) -> pd.DataFrame:
        """Return historical data for *ticker* between *start* and *end*.

        Parameters
        ----------
        ticker:
            Ticker symbol or list of symbols understood by yfinance.
        start:
            Inclusive start date in ``YYYY-MM-DD`` format.
        end:
            Exclusive end date in ``YYYY-MM-DD`` format.
        """
        tickers = (
            [ticker]
            if isinstance(ticker, str)
            else list(ticker)
        )
        cache_key = "-".join(tickers)
        cache_file = self.cache_dir / f"{cache_key}.parquet"

        if cache_file.exists():
            df = pd.read_parquet(cache_file)
        else:
            df = yf.download(
                tickers,
                start=start,
                end=end,
                progress=False,
                auto_adjust=False,
            )
            if df.empty:
                raise ValueError(
                    f"No data returned for ticker '{cache_key}'"
                )

            df.index.name = "date"

            if isinstance(df.columns, pd.MultiIndex):
                df = df.swaplevel(0, 1, axis=1)
                mask = df.columns.get_level_values(1) == "Close"
                df = df.loc[:, mask]
                df.columns = [str(c[0]) for c in df.columns]
            else:
                lower = [str(c).lower() for c in df.columns]
                ohlcv = {"open", "high", "low", "close", "adj close", "volume"}
                if set(lower) <= ohlcv:
                    df.columns = pd.Index(lower)
                else:
                    df.columns = pd.Index([str(c) for c in df.columns])

            df.to_parquet(cache_file)

        df.index.name = "date"
        df = df.loc[pd.Timestamp(start) : pd.Timestamp(end)]

        if isinstance(df.columns, pd.MultiIndex):
            df = df.swaplevel(0, 1, axis=1)
            mask = df.columns.get_level_values(1) == "Close"
            df = df.loc[:, mask]
            df.columns = [str(c[0]) for c in df.columns]
        else:
            lower = [str(c).lower() for c in df.columns]
            ohlcv = {"open", "high", "low", "close", "adj close", "volume"}
            if set(lower) <= ohlcv:
                df.columns = pd.Index(lower)
            else:
                df.columns = pd.Index([str(c) for c in df.columns])

        return df
