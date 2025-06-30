from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.macd import MACDStrategy  # noqa: E402


def test_macd_strategy_basic_signals() -> None:
    index = pd.date_range("2023-01-02", periods=20, freq="B")
    closes = [1] * 5 + [10] * 5 + [5] * 5 + [15] * 5
    data = pd.DataFrame({"close": closes}, index=index)
    strategy = MACDStrategy(fast=2, slow=3, signal=2)
    signals = [strategy.next_bar(row) for _, row in data.iterrows()]
    assert "BUY" in signals and "SELL" in signals


def test_macd_invalid_index() -> None:
    strategy = MACDStrategy()
    bar = pd.Series({"close": 1.0}, name=0)
    with pytest.raises(ValueError):
        strategy.next_bar(bar)


def test_macd_hold_initially() -> None:
    index = pd.date_range("2023-01-02", periods=2, freq="B")
    closes = [1, 2]
    strategy = MACDStrategy(fast=2, slow=3, signal=2)
    signals = [
        strategy.next_bar(pd.Series({"close": c}, name=i))
        for i, c in zip(index, closes)
    ]
    assert signals[0] == "HOLD"
