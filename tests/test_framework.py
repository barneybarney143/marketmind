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


def test_downloader_caches(tmp_path: Path) -> None:
    downloader = DataDownloader(cache_dir=tmp_path)

    df = downloader.get_history("SPY", "2020-01-01", "2020-01-10")
    assert (tmp_path / "SPY.parquet").exists()
    df2 = downloader.get_history("SPY", "2020-01-01", "2020-01-10")
    assert len(df) == len(df2)


def test_downloader_multi_ticker(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    downloader = DataDownloader(cache_dir=tmp_path)

    def fake_download(*args: Any, **kwargs: Any) -> pd.DataFrame:
        index = pd.date_range("2020-01-01", periods=3, freq="D")
        arrays = [("Close", "AAA"), ("Close", "BBB")]
        cols = pd.MultiIndex.from_tuples(arrays, names=["Price", "Ticker"])
        return pd.DataFrame([[1, 2], [2, 1], [3, 0]], index=index, columns=cols)

    monkeypatch.setattr(yf, "download", fake_download)

    df = downloader.get_history(["AAA", "BBB"], "2020-01-01", "2020-01-04")
    assert list(df.columns) == ["AAA", "BBB"]
    assert len(df) == 3


class DummyStrategy(Strategy):
    def next_bar(self, bar: pd.Series[Any]) -> str:
        return "HOLD"


def test_backtester_length(tmp_path: Path) -> None:
    downloader = DataDownloader(cache_dir=tmp_path)
    data = downloader.get_history("SPY", "2020-01-01", "2020-01-10")

    strategy = DummyStrategy()
    bt = Backtester(strategy, data)
    results = bt.run()
    assert len(results) == len(data)
