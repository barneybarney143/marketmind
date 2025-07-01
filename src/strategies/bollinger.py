from __future__ import annotations

from typing import Any

import pandas as pd

from .base import HistoryStrategy


class BollingerStrategy(HistoryStrategy):
    """Weekly Bollinger Band mean-reversion strategy."""

    def __init__(self, length: int = 20, dev: float = 2.0) -> None:
        super().__init__(length=length, dev=dev)
        self.length = length
        self.dev = dev



    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError("Bar index must be a pd.Timestamp for Bollinger strategy")
        close = float(bar["close"])
        self._close_history.at[bar.name] = close

        weekly_close = self._close_history.resample("W-FRI").last()
        ma = weekly_close.rolling(self.length).mean()
        std = weekly_close.rolling(self.length).std()
        lower_band = ma - self.dev * std

        last_close = float(weekly_close.iloc[-1])
        lb = lower_band.iloc[-1]
        mid = ma.iloc[-1]

        if pd.isna(lb) or pd.isna(mid):
            return "HOLD"

        if last_close < float(lb):
            return "BUY"
        if last_close >= float(mid):
            return "SELL"
        return "HOLD"
