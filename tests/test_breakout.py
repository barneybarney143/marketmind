from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.breakout import BreakoutStrategy  # noqa: E402


def test_breakout_buy_and_stop() -> None:
    index = pd.date_range("2023-01-02", periods=20, freq="B")
    closes = [100] * 10 + [110] * 5 + [90] * 5
    data = pd.DataFrame({"close": closes}, index=index)

    strategy = BreakoutStrategy(lookback_weeks=2, stop_pct=0.1)
    signals = [strategy.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals
    assert "SELL" in signals


def test_breakout_sma_exit() -> None:
    index = pd.date_range("2023-01-02", periods=202, freq="B")
    closes = [100.0] * 200 + [110.0, 99.5]
    data = pd.DataFrame({"close": closes}, index=index)

    strategy = BreakoutStrategy(lookback_weeks=1, stop_pct=0.1)
    signals = [strategy.next_bar(row) for _, row in data.iterrows()]

    assert signals[-1] == "SELL"

