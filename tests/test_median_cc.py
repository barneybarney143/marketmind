from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.median_cc import CoveredCallMedianStrategy  # noqa: E402


def test_cc_median_signals() -> None:
    index = pd.date_range("2024-01-02", periods=80, freq="B")
    closes = [100] * 60 + [80] * 10 + [110] * 10
    data = pd.DataFrame({"close": closes}, index=index)

    strat = CoveredCallMedianStrategy(band=1.0)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals and "SELL" in signals
