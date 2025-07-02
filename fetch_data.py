"""Simple data fetch helper wrapping :class:`DataDownloader`."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

from data import DataDownloader

# Map of non-UCITS tickers to their UCITS equivalents
_UCITS = {"SPY": "CSP1"}

__all__ = ["fetch"]


def fetch(
    tickers: str | Iterable[str],
    start: str = "2000-01-01",
    end: str | None = None,
    interval: str = "1d",
    ucits_map: bool = True,
) -> dict[str, pd.DataFrame]:
    """Return historical OHLCV data for ``tickers``.

    Args:
        tickers: A ticker symbol or list of symbols.
        start: ISO formatted start date.
        end: ISO formatted end date. Defaults to today when ``None``.
        interval: Bar interval (unused, kept for API compatibility).
        ucits_map: Map symbols to their UCITS equivalent when ``True``.

    Returns:
        Mapping of canonical ticker to :class:`pandas.DataFrame` with OHLCV data.
    """
    symbols = [tickers] if isinstance(tickers, str) else list(tickers)
    if end is None:
        end = datetime.utcnow().date().isoformat()

    downloader = DataDownloader()
    result: dict[str, pd.DataFrame] = {}
    for sym in symbols:
        remote = _UCITS.get(sym, sym) if ucits_map else sym
        df = downloader.get_history(remote, start, end)
        result[sym] = df
    return result


def _main() -> None:
    import sys

    args = sys.argv[1:]
    if not args:
        print("Usage: python -m fetch_data TICKER [TICKER...]")
        raise SystemExit(1)
    data = fetch(args)
    for ticker, df in data.items():
        out = Path(f"{ticker}.csv")
        df.to_csv(out)
        print(f"Wrote {out}")


if __name__ == "__main__":
    _main()
