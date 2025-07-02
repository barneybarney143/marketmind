from __future__ import annotations

from typing import Any

import pandas as pd

from .base import HistoryStrategy


class LeveragedTrendStrategy(HistoryStrategy):
    """Simple trend-following strategy using a leveraged S&P 500 ETF."""

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

        weeks = max(1, self.sma_len // 5)
        weekly_close = self._close_history.resample("W-FRI").last()
        sma = weekly_close.rolling(weeks).mean().iloc[-1]

        if pd.isna(sma):
            return "HOLD"

        current = float(weekly_close.iloc[-1])
        if self.position == 0 and current > float(sma):
            self.position = 1
            return "BUY"
        if self.position == 1 and current <= float(sma):
            self.position = 0
            return "SELL"
        return "HOLD"
