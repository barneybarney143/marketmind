from __future__ import annotations

from typing import Any

import pandas as pd

from .base import Strategy as BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """52-week high breakout momentum strategy."""

    def __init__(self, lookback_weeks: int = 52, stop_pct: float = 0.08) -> None:
        super().__init__(lookback_weeks=lookback_weeks, stop_pct=stop_pct)
        self.lookback_weeks = lookback_weeks
        self.stop_pct = stop_pct
        self._close_history = pd.Series(dtype=float)
        self._highest_close: float | None = None

    def reset(self) -> None:
        super().reset()
        self._close_history = pd.Series(dtype=float)
        self._highest_close = None

    def next_bar(self, bar: pd.Series[Any]) -> str:
        """Return trading signal based on breakout logic."""
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError("Bar index must be a pd.Timestamp for Breakout strategy")
        close = float(bar["close"])
        self._close_history.at[bar.name] = close

        weekly_close = self._close_history.resample("W-FRI").last()
        current_week_close = float(weekly_close.iloc[-1])
        lookback_window = weekly_close.iloc[-self.lookback_weeks - 1 : -1]
        if lookback_window.empty:
            highest_weekly_close = float("-inf")
        else:
            highest_weekly_close = float(lookback_window.max())

        sma_200 = self._close_history.rolling(window=200).mean().iloc[-1]
        sma_200_value: float | None = float(sma_200) if not pd.isna(sma_200) else None

        signal = "HOLD"
        if self.position == 0:
            if current_week_close > highest_weekly_close:
                signal = "BUY"
                self.position = 1
                self._highest_close = current_week_close
        else:
            if self._highest_close is None:
                self._highest_close = current_week_close
            self._highest_close = max(self._highest_close, current_week_close)
            stop_level = self._highest_close * (1 - self.stop_pct)
            if current_week_close < stop_level:
                signal = "SELL"
                self.position = 0
                self._highest_close = None
            elif sma_200_value is not None and close < sma_200_value:
                signal = "SELL"
                self.position = 0
                self._highest_close = None
        return signal
