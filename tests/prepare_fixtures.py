
"""Download small OHLCV samples for unit tests."""

from __future__ import annotations

from pathlib import Path
import tempfile
import shutil

import pandas as pd

from data import DataDownloader

TICKERS = ["SPY"]
N_DAYS = 120


def build_sample(ticker: str, days: int, dest: Path) -> None:
    """Download *days* of data for *ticker* and save CSV."""
    cache_dir = Path(tempfile.mkdtemp())
    try:
        downloader = DataDownloader(cache_dir=cache_dir)
        end = pd.Timestamp.today().strftime("%Y-%m-%d")
        start = (pd.Timestamp.today() - pd.Timedelta(days=days)).strftime(
            "%Y-%m-%d"
        )
        df = downloader.get_history(ticker, start, end)
        used_cols = ["open", "high", "low", "close", "adj_close", "volume"]
        df = df[used_cols].head(500)
        dest.mkdir(exist_ok=True)
        df.to_csv(dest / f"sample_{ticker}.csv", index=False)
    finally:
        shutil.rmtree(cache_dir, ignore_errors=True)


def main() -> None:
    dest = Path(__file__).with_name("test_data")
    for ticker in TICKERS:
        build_sample(ticker, N_DAYS, dest)


if __name__ == "__main__":
    main()
