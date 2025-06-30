from __future__ import annotations

from typing import List

import pandas as pd

from strategies.base import Strategy


class Backtester:
    """Simple long-only back-testing engine."""

    def __init__(self, strategy: Strategy, data: pd.DataFrame) -> None:
        self.strategy = strategy
        self.data = data
        self.position = 0
        self.equity = 1.0
        self.trades: List[tuple[str, pd.Timestamp, float]] = []

    def run(self) -> pd.DataFrame:
        """Run the back-test and return equity curve."""
        self.strategy.reset()
        results = []
        peak = self.equity
        prev_close: float | None = None
        for date, row in self.data.iterrows():
            ts = pd.Timestamp(str(date))
            signal = self.strategy.next_bar(row)
            price = float(row["close"])
            if signal == "BUY" and self.position == 0:
                self.position = 1
                self.trades.append(("BUY", ts, price))
            elif signal == "SELL" and self.position == 1:
                self.position = 0
                self.trades.append(("SELL", ts, price))
            if prev_close is None:
                ret = 0.0
            else:
                ret = (price - prev_close) / prev_close
            self.equity *= 1 + ret * self.position
            peak = max(peak, self.equity)
            drawdown = self.equity / peak - 1
            results.append(
                {
                    "date": ts,
                    "price": price,
                    "position": self.position,
                    "signal": signal,
                    "equity": self.equity,
                    "drawdown": drawdown,
                }
            )
            prev_close = price
        return pd.DataFrame(results).set_index("date")
