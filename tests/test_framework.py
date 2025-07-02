from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from typing import Any

import pytest
import yfinance as yf

import pandas as pd

from data import DataDownloader
from engine import Backtester
from strategies.base import Strategy


def test_downloader_caches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    downloader = DataDownloader(cache_dir=tmp_path)

    def fake_download(*args: Any, **kwargs: Any) -> pd.DataFrame:
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

    df = downloader.get_history("SPY", "2020-01-01", "2020-01-10")
    cache_file = tmp_path / "CSPX-2020-01-01-2020-01-10.parquet"
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


def test_backtester_length(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    downloader = DataDownloader(cache_dir=tmp_path)

    def fake_download(*args: Any, **kwargs: Any) -> pd.DataFrame:
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

    data = downloader.get_history("SPY", "2020-01-01", "2020-01-10")

    strategy = DummyStrategy()
    bt = Backtester(strategy, data)
    results = bt.run()
    assert len(results) == len(data)
