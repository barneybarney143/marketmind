from __future__ import annotations

from typing import Any

import pandas as pd

from .base import HistoryStrategy


def wilder_rsi(series: pd.Series[float], length: int = 14) -> pd.Series[float]:
    """Compute Wilder's RSI."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - 100 / (1 + rs)
    zero_mask = (avg_gain == 0) & (avg_loss == 0)
    rsi = rsi.where(~zero_mask, 50.0)
    return rsi


class RSIStrategy(HistoryStrategy):
    """Weekly RSI mean-reversion strategy."""

    def __init__(
        self, rsi_buy: float = 30, rsi_sell: float = 70, length: int = 14
    ) -> None:
        super().__init__(rsi_buy=rsi_buy, rsi_sell=rsi_sell, length=length)
        self.rsi_buy = rsi_buy
        self.rsi_sell = rsi_sell
        self.length = length

    def next_bar(self, bar: pd.Series[Any]) -> str:
        """Return trading signal based on weekly RSI."""
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError("Bar index must be a pd.Timestamp for RSI strategy")
        close = float(bar["close"])
        self._close_history.at[bar.name] = close

        weekly_close = self._close_history.resample("W-FRI").last()
        rsi_series = wilder_rsi(weekly_close, self.length)
        clean_rsi = rsi_series.dropna()
        rsi_value = clean_rsi.iloc[-1] if not clean_rsi.empty else None

        if rsi_value is None:
            return "HOLD"
        if rsi_value <= self.rsi_buy:
            return "BUY"
        if rsi_value >= self.rsi_sell:
            return "SELL"
        return "HOLD"
