from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.covered_call_median import CoveredCallMedianStrategy  # noqa: E402


def test_covered_call_median_signals() -> None:
    index = pd.date_range("2024-01-02", periods=70, freq="B")
    closes = [100.0] * 60 + [98.0, 102.0] + [100.0] * 8
    data = pd.DataFrame({"close": closes}, index=index)
    strat = CoveredCallMedianStrategy(band=1.0, window=60)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals
    assert "SELL" in signals

