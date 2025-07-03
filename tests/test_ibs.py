from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.ibs import IBSStrategy  # noqa: E402


def test_ibs_signals() -> None:
    strategy = IBSStrategy(buy_thr=0.2, sell_thr=0.8)
    bars = [
        pd.Series({"open": 0, "high": 10, "low": 0, "close": 2}),
        pd.Series({"open": 0, "high": 10, "low": 0, "close": 8}),
        pd.Series({"open": 0, "high": 10, "low": 0, "close": 5}),
    ]

    signals = [strategy.next_bar(bar) for bar in bars]

    assert signals == ["BUY", "SELL", "HOLD"]


def test_ibs_prefixed_columns() -> None:
    strategy = IBSStrategy()
    bar = pd.Series(
        {
            "spy_open": 1,
            "spy_high": 10,
            "spy_low": 0,
            "spy_close": 9,
        }
    )
    assert strategy.next_bar(bar) == "SELL"
