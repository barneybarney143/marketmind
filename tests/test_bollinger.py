from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.bollinger import BollingerStrategy  # noqa: E402


def test_bollinger_strategy_signals() -> None:
    index = pd.date_range("2023-01-02", periods=20, freq="B")
    closes = [100] * 5 + [102] * 5 + [90] * 5 + [100] * 5
    data = pd.DataFrame({"close": closes}, index=index)

    strategy = BollingerStrategy(length=2, dev=0.5)
    signals = [strategy.next_bar(row) for _, row in data.iterrows()]

    assert "BUY" in signals and "SELL" in signals
