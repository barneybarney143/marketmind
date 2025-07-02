from __future__ import annotations

from typing import Any

import pandas as pd
from pandas.tseries.offsets import BDay, BMonthEnd

from .base import Strategy


class EndOfMonthBondPopStrategy(Strategy):
    """Hold bonds for the last N trading days of each month."""

    def __init__(self, hold_days: int = 7) -> None:
        super().__init__(hold_days=hold_days)
        self.hold_days = hold_days

    @staticmethod
    def _last_bday(ts: pd.Timestamp) -> pd.Timestamp:
        offset = BMonthEnd()
        target = ts if ts.is_month_end else ts + offset
        return pd.Timestamp(offset.rollback(target))

    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError(
                "Bar index must be a pd.Timestamp for EndOfMonthBondPop strategy"
            )
        ts = bar.name
        last_bday = self._last_bday(ts)
        start_hold = last_bday - BDay(self.hold_days - 1)
        in_window = start_hold <= ts <= last_bday

        if in_window and self.position == 0:
            self.position = 1
            return "BUY"
        if not in_window and self.position == 1:
            self.position = 0
            return "SELL"
        return "HOLD"

