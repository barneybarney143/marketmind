from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd
import pytest
import yfinance as yf

from data import DataDownloader
from engine import Backtester
from strategies.base import Strategy

SAMPLE_DIR = Path(__file__).with_name("test_data")


def load_sample(ticker: str) -> pd.DataFrame:
    """Return fixture data for *ticker* with a synthetic index."""
    df = pd.read_csv(SAMPLE_DIR / f"sample_{ticker}.csv")
    df.index = pd.date_range("2024-01-01", periods=len(df), freq="D")
    return df

def test_downloader_caches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    downloader = DataDownloader(cache_dir=tmp_path)

    sample = load_sample("SPY")

    monkeypatch.setattr(yf, "download", lambda *args, **kwargs: sample)

    df = downloader.get_history("SPY", "2020-01-01", "2020-01-10")
    cache_file = tmp_path / "SPY-2020-01-01-2020-01-10.parquet"
    assert cache_file.exists()
    df2 = downloader.get_history("SPY", "2020-01-01", "2020-01-10")
    assert len(df) == len(df2)


def test_downloader_multi_ticker(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    downloader = DataDownloader(cache_dir=tmp_path)

    def fake_download(ticker: str, *args: Any, **kwargs: Any) -> pd.DataFrame:
        index = pd.date_range("2020-01-01", periods=3, freq="D")
        data = {
            "Open": [1, 2, 3],
            "High": [1, 2, 3],
            "Low": [1, 2, 3],
            "Close": [1, 2, 3],
            "Adj Close": [1, 2, 3],
            "Volume": [1, 1, 1],
        }
        return pd.DataFrame(data, index=index)

    monkeypatch.setattr(yf, "download", fake_download)

    df = downloader.get_history(["AAA", "BBB"], "2020-01-01", "2020-01-04")
    expected_cols = [
        f"aaa_{c}"
        for c in ["open", "high", "low", "close", "adj_close", "volume"]
    ] + [
        f"bbb_{c}"
        for c in ["open", "high", "low", "close", "adj_close", "volume"]
    ]
    assert list(df.columns) == expected_cols
    assert len(df) == 3


class DummyStrategy(Strategy):
    def next_bar(self, bar: pd.Series[Any]) -> str:
        return "HOLD"


def test_backtester_length() -> None:
    data = load_sample("SPY")

    strategy = DummyStrategy()
    bt = Backtester(strategy, data)
    results = bt.run()
    assert len(results) == len(data)
