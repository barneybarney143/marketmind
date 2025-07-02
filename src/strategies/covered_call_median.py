from __future__ import annotations

from typing import Any

import pandas as pd

from .base import HistoryStrategy


class CoveredCallMedianStrategy(HistoryStrategy):
    """Median band strategy for a covered call ETF."""

    def __init__(self, band: float = 1.0, window: int = 60) -> None:
        super().__init__(band=band, window=window)
        self.band = band
        self.window = window

    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError(
                "Bar index must be a pd.Timestamp for CoveredCallMedian strategy"
            )
        close = float(bar["close"])
        self._close_history.at[bar.name] = close

        median = self._close_history.rolling(self.window).median().iloc[-1]
        if pd.isna(median):
            return "HOLD"

        lower = float(median) * (1 - self.band / 100)
        upper = float(median) * (1 + self.band / 100)

        if close <= lower:
            return "BUY"
        if close >= upper:
            return "SELL"
        return "HOLD"

