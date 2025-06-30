from __future__ import annotations

from typing import Any

import pandas as pd

from .base import Strategy as BaseStrategy


class MACDStrategy(BaseStrategy):
    """Moving Average Convergence Divergence crossover strategy."""

    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9) -> None:
        super().__init__(fast=fast, slow=slow, signal=signal)
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self._close_history = pd.Series(dtype=float)

    def reset(self) -> None:
        super().reset()
        self._close_history = pd.Series(dtype=float)

    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError("Bar index must be a pd.Timestamp for MACD strategy")
        close = float(bar["close"])
        self._close_history.at[bar.name] = close

        weekly_close = self._close_history.resample("W-FRI").last()
        ema_fast = weekly_close.ewm(span=self.fast, adjust=False).mean()
        ema_slow = weekly_close.ewm(span=self.slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal, adjust=False).mean()

        if len(macd_line) < 2:
            return "HOLD"

        prev_macd = macd_line.iloc[-2]
        prev_signal = signal_line.iloc[-2]
        curr_macd = macd_line.iloc[-1]
        curr_signal = signal_line.iloc[-1]

        if prev_macd <= prev_signal and curr_macd > curr_signal:
            return "BUY"
        if prev_macd >= prev_signal and curr_macd < curr_signal:
            return "SELL"
        return "HOLD"


Strategy = MACDStrategy
