from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.eom_bond import EndOfMonthBondPopStrategy  # noqa: E402


def test_eom_bond_signals() -> None:
    index = pd.date_range("2024-01-02", periods=40, freq="B")
    closes = list(range(40))
    data = pd.DataFrame({"close": closes}, index=index)

    strat = EndOfMonthBondPopStrategy(hold_days=5)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals and "SELL" in signals
