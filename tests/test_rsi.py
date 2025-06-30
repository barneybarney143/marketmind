from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.rsi import RSIStrategy, wilder_rsi  # noqa: E402


def test_wilder_rsi_constant_series() -> None:
    index = pd.date_range("2023-01-06", periods=20, freq="W-FRI")
    series = pd.Series(100.0, index=index)
    rsi = wilder_rsi(series, length=14)
    assert rsi.dropna().iloc[-1] == 50


def test_rsi_strategy_signals() -> None:
    index = pd.date_range("2023-01-02", periods=30, freq="B")
    close = pd.Series(range(30), index=index, name="close")
    data = pd.DataFrame({"close": close})
    strategy = RSIStrategy(rsi_buy=30, rsi_sell=70, length=2)
    signals = [strategy.next_bar(row) for _, row in data.iterrows()]
    assert signals[0] == "HOLD"
    assert "BUY" in signals or "SELL" in signals
