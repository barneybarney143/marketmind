from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.leveragedtrend import LeveragedTrendStrategy  # noqa: E402


def test_leveragedtrend_signals() -> None:
    index = pd.date_range("2024-01-02", periods=60, freq="B")
    closes = [10.0] * 20 + [20.0] * 20 + [5.0] * 20
    data = pd.DataFrame({"close": closes}, index=index)
    strat = LeveragedTrendStrategy(sma_len=4)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals
    assert "SELL" in signals

