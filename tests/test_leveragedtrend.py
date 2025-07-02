from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.leveragedtrend import LeveragedTrendStrategy  # noqa: E402


def test_leveragedtrend_signals() -> None:
    index = pd.date_range("2023-01-02", periods=260, freq="B")
    prices = [100] * 220 + [110] * 20 + [90] * 20
    data = pd.DataFrame({"close": prices}, index=index)

    strat = LeveragedTrendStrategy(sma_len=200)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals and "SELL" in signals
