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
        high_col = "high"
        low_col = "low"
        close_col = "close"

        if high_col not in bar.index:
            prefixes = {
                c.removesuffix("_high")
                for c in bar.index
                if c.endswith("_high")
            }
            prefixes &= {
                c.removesuffix("_low")
                for c in bar.index
                if c.endswith("_low")
            }
            prefixes &= {
                c.removesuffix("_close")
                for c in bar.index
                if c.endswith("_close")
            }

            if len(prefixes) == 1:
                prefix = prefixes.pop()
                high_col = f"{prefix}_high"
                low_col = f"{prefix}_low"
                close_col = f"{prefix}_close"
            else:
                raise KeyError("Missing high/low/close columns")

        high = float(bar[high_col])
        low = float(bar[low_col])
        close = float(bar[close_col])

        if high == low:
            ibs = 0.5
        else:
            ibs = (close - low) / (high - low)

        if ibs <= self.buy_thr:
            return "BUY"
        if ibs >= self.sell_thr:
            return "SELL"
        return "HOLD"
