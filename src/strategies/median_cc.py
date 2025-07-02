from __future__ import annotations

from typing import Any

import pandas as pd

from .base import HistoryStrategy


class CoveredCallMedianStrategy(HistoryStrategy):
    """Median-reversion strategy for a covered call ETF."""

    def __init__(self, band: float = 0.01, median_len: int = 60) -> None:
        super().__init__(band=band, median_len=median_len)
        self.band = band / 100 if band >= 1 else band
        self.median_len = median_len

    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError(
                "Bar index must be a pd.Timestamp for CoveredCallMedian strategy"
            )
        close = float(bar["close"])
        self._close_history.at[bar.name] = close

        med = self._close_history.rolling(self.median_len).median().iloc[-1]
        if pd.isna(med):
            return "HOLD"

        lower = float(med) * (1 - self.band)
        upper = float(med) * (1 + self.band)

        if self.position == 0 and close <= lower:
            self.position = 1
            return "BUY"
        if self.position == 1 and close >= upper:
            self.position = 0
            return "SELL"
        return "HOLD"
