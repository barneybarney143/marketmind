from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from engine import Backtester  # noqa: E402
from strategies.dual_mom import DualMomentumStrategy  # noqa: E402


def test_dual_mom_signals() -> None:
    index = pd.date_range("2023-01-01", periods=90, freq="D")
    data = pd.DataFrame({"AAA": range(90), "BBB": range(90, 0, -1)}, index=index)

    strategy = DualMomentumStrategy(["AAA", "BBB"], lookback_weeks=1)
    signals = [strategy.next_bar(row) for _, row in data.iterrows()]

    jan_end = pd.Timestamp("2023-01-31")
    assert signals[index.get_loc(jan_end)] == "BUY:AAA"


def test_backtester_multi_asset() -> None:
    index = pd.date_range("2023-01-01", periods=40, freq="D")
    data = pd.DataFrame({"AAA": range(40), "BBB": range(40, 0, -1)}, index=index)
    strategy = DualMomentumStrategy(["AAA", "BBB"], lookback_weeks=1)
    bt = Backtester(strategy, data)
    results = bt.run()
    assert len(results) == len(data)
    assert any(t[0] == "BUY" for t in bt.trades)
