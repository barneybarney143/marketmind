from __future__ import annotations

from typing import Any, Iterable

import pandas as pd

from .base import Strategy as BaseStrategy


class DualMomentumStrategy(BaseStrategy):
    """Simple dual momentum ETF rotation strategy."""

    def __init__(
        self, universe: Iterable[str], lookback_weeks: int = 26, top_k: int = 1
    ) -> None:
        self.universe = list(universe)
        self.lookback_weeks = lookback_weeks
        self.top_k = top_k
        self._close_history: dict[str, pd.Series[float]] = {}
        self._current_symbol: str | None = None
        super().__init__(
            universe=self.universe, lookback_weeks=lookback_weeks, top_k=top_k
        )

    def reset(self) -> None:
        super().reset()
        self._close_history = {t: pd.Series(dtype=float) for t in self.universe}
        self._current_symbol = None

    @staticmethod
    def _is_month_end(ts: pd.Timestamp) -> bool:
        return (ts + pd.Timedelta(days=1)).month != ts.month

    def next_bar(self, bar: pd.Series[Any]) -> str:
        if not isinstance(bar.name, pd.Timestamp):
            raise ValueError(
                "Bar index must be a pd.Timestamp for DualMomentum strategy"
            )
        ts = bar.name
        for ticker in self.universe:
            series = self._close_history.setdefault(ticker, pd.Series(dtype=float))
            series.at[ts] = float(bar[ticker])

        signal = "HOLD"
        if self._is_month_end(ts):
            weekly = {
                t: series.resample("W-FRI").last()
                for t, series in self._close_history.items()
            }
            trailing: dict[str, float] = {}
            for t, series in weekly.items():
                if len(series) < self.lookback_weeks + 1:
                    trailing[t] = float("-inf")
                else:
                    start = float(series.iloc[-self.lookback_weeks - 1])
                    end = float(series.iloc[-1])
                    trailing[t] = (end - start) / start
            ranked = sorted(trailing, key=lambda t: trailing[t], reverse=True)
            winners = [t for t in ranked[: self.top_k] if trailing[t] > 0]
            new_symbol = winners[0] if winners else None
            if new_symbol is None:
                if self._current_symbol is not None:
                    signal = f"SELL:{self._current_symbol}"
                    self._current_symbol = None
            elif new_symbol != self._current_symbol:
                signal = f"BUY:{new_symbol}"
                self._current_symbol = new_symbol
        return signal


Strategy = DualMomentumStrategy
