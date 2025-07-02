from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.eom_bond import EndOfMonthBondPopStrategy  # noqa: E402


def test_eom_bond_buy_sell() -> None:
    index = pd.date_range("2024-01-22", periods=10, freq="B")
    data = pd.DataFrame({"close": 100.0}, index=index)
    strat = EndOfMonthBondPopStrategy(hold_days=2)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals
    assert "SELL" in signals

