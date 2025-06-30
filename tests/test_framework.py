from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from typing import Any

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
