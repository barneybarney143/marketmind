from __future__ import annotations

from typing import Any

import pandas as pd

from .base import HistoryStrategy


class LeveragedTrendStrategy(HistoryStrategy):
    """Trend-following on 2x S&P 500 ETF."""

    def __init__(self, sma_len: int = 200) -> None:
        super().__init__(sma_len=sma_len)
        self.sma_len = sma_len

    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError(
                "Bar index must be a pd.Timestamp for LeveragedTrend strategy"
            )
        close = float(bar["close"])
        self._close_history.at[bar.name] = close

        weekly_close = self._close_history.resample("W-FRI").last()
        sma = weekly_close.rolling(self.sma_len).mean()
        sma_val = sma.iloc[-1]

        if pd.isna(sma_val):
            return "HOLD"

        if close > float(sma_val):
            if self.position == 0:
                self.position = 1
                return "BUY"
        else:
            if self.position == 1:
                self.position = 0
                return "SELL"
        return "HOLD"

