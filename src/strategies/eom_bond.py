from __future__ import annotations

from typing import Any

import pandas as pd
from pandas.tseries.offsets import BDay, BMonthEnd

from .base import Strategy


class EndOfMonthBondPopStrategy(Strategy):
    """Hold a Treasury ETF only for the last ``hold_days`` of each month."""

    def __init__(self, hold_days: int = 7) -> None:
        super().__init__(hold_days=hold_days)
        self.hold_days = hold_days

    @staticmethod
    def _in_window(ts: pd.Timestamp, hold_days: int) -> bool:
        end = ts + BMonthEnd(0)
        start = end - BDay(hold_days - 1)
        return start <= ts <= end

    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError(
                "Bar index must be a pd.Timestamp for EndOfMonthBondPop strategy"
            )
        ts = bar.name
        active = self._in_window(ts, self.hold_days)
        if self.position == 0 and active:
            self.position = 1
            return "BUY"
        if self.position == 1 and not active:
            self.position = 0
            return "SELL"
        return "HOLD"
