from __future__ import annotations

from typing import Any

import pandas as pd
from pandas.tseries.offsets import BMonthEnd

from .base import Strategy


class HFEA55Strategy(Strategy):
    """Hold 55% S&P 500 3× and 45% 10yr Treasury 3×, rebalanced monthly."""

    def __init__(self, rebalance_days: int = 21) -> None:
        super().__init__(rebalance_days=rebalance_days)
        self.rebalance_days = rebalance_days
        self._last_rebalance: pd.Timestamp | None = None

    @staticmethod
    def _is_month_end(ts: pd.Timestamp) -> bool:
        return bool(ts == (ts + BMonthEnd(0)))

    def next_bar(self, bar: pd.Series[Any]) -> dict[str, float] | str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError(
                "Bar index must be a pd.Timestamp for HFEA55 strategy"
            )
        ts = bar.name
        if self._last_rebalance is None:
            self._last_rebalance = ts
            return {"3USL": 0.55, "3TYL": 0.45}
        if self._is_month_end(ts) and (
            ts - self._last_rebalance
        ).days >= self.rebalance_days:
            self._last_rebalance = ts
            return {"3USL": 0.55, "3TYL": 0.45}
        return {}
