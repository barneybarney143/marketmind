from __future__ import annotations

from typing import Any

import pandas as pd

from .base import Strategy as BaseStrategy


class IBSStrategy(BaseStrategy):
    """Internal Bar Strength strategy."""

    def __init__(self, buy_thr: float = 0.2, sell_thr: float = 0.8) -> None:
        super().__init__(buy_thr=buy_thr, sell_thr=sell_thr)
        self.buy_thr = buy_thr
        self.sell_thr = sell_thr

    def next_bar(self, bar: pd.Series[Any]) -> str:
        """Return trading signal based on IBS."""
        high = float(bar["high"])
        low = float(bar["low"])
        close = float(bar["close"])

        if high == low:
            ibs = 0.5
        else:
            ibs = (close - low) / (high - low)

        if ibs <= self.buy_thr:
            return "BUY"
        if ibs >= self.sell_thr:
            return "SELL"
        return "HOLD"


Strategy = IBSStrategy
