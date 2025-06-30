from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.macd import MACDStrategy  # noqa: E402


def test_macd_strategy_signals() -> None:
    index = pd.date_range("2023-01-02", periods=20, freq="B")
    closes = [1] * 5 + [10] * 5 + [5] * 5 + [15] * 5
    data = pd.DataFrame({"close": closes}, index=index)
    strategy = MACDStrategy(fast=2, slow=3, signal=2)

    signals = [strategy.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals and "SELL" in signals
