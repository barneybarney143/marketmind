from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from .base import Strategy


class HFEA55Strategy(Strategy):
    """55/45 split between 3x S&P 500 and 3x Treasuries."""

    def __init__(self, rebalance_days: int = 21) -> None:
        super().__init__(rebalance_days=rebalance_days)
        self.rebalance_days = rebalance_days
        self._counter = 0

    def next_bar(self, bar: pd.Series[Any]) -> Dict[str, float] | str:  # type: ignore[override]
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError("Bar index must be a pd.Timestamp for HFEA55 strategy")

        self._counter += 1
        if self._counter >= self.rebalance_days or self.position == 0:
            self._counter = 0
            self.position = 1
            return {"3USL": 0.55, "3TYL": 0.45}

        return "HOLD"

