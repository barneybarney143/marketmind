from __future__ import annotations

from typing import Dict, List

import pandas as pd

from strategies.base import Strategy


class Backtester:
    """Simple long-only back-testing engine."""

    def __init__(self, strategy: Strategy, data: pd.DataFrame) -> None:
        self.strategy = strategy
        self.data = data
        self.position = 0
        self.symbol: str | None = None
        self.equity = 1.0
        self.trades: List[tuple[str, str, pd.Timestamp, float]] = []
        self._multi_asset = "close" not in self.data.columns

    def run(self) -> pd.DataFrame:
        """Run the back-test and return equity curve."""
        self.strategy.reset()
        results = []
        peak = self.equity
        prev_close: Dict[str, float | None] = {col: None for col in self.data.columns}
        for date, row in self.data.iterrows():
            ts = pd.Timestamp(str(date))

            # compute return for current holding before processing today's signal
            if self.position == 1 and self.symbol is not None:
                price = float(row[self.symbol])
                pc = prev_close.get(self.symbol)
                ret = 0.0 if pc is None else (price - pc) / pc
            else:
                price = float(row["close"]) if not self._multi_asset else 0.0
                ret = 0.0

            self.equity *= 1 + ret
            peak = max(peak, self.equity)
            drawdown = self.equity / peak - 1

            signal = self.strategy.next_bar(row)

            if self._multi_asset:
                if signal.startswith("BUY:"):
                    ticker = signal.split(":", 1)[1]
                    if (
                        self.position == 1
                        and self.symbol is not None
                        and self.symbol != ticker
                    ):
                        sell_price = float(row[self.symbol])
                        self.trades.append(("SELL", self.symbol, ts, sell_price))
                    if self.symbol != ticker:
                        buy_price = float(row[ticker])
                        self.trades.append(("BUY", ticker, ts, buy_price))
                        self.position = 1
                        self.symbol = ticker
                elif signal.startswith("SELL:"):
                    ticker = signal.split(":", 1)[1]
                    if self.position == 1 and self.symbol == ticker:
                        sell_price = float(row[ticker])
                        self.trades.append(("SELL", ticker, ts, sell_price))
                        self.position = 0
                        self.symbol = None
            else:
                if signal == "BUY" and self.position == 0:
                    self.position = 1
                    self.symbol = "close"
                    buy_price = float(row["close"])
                    self.trades.append(("BUY", "close", ts, buy_price))
                elif signal == "SELL" and self.position == 1:
                    self.position = 0
                    sell_price = float(row["close"])
                    self.trades.append(("SELL", "close", ts, sell_price))

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

            for col in self.data.columns:
                prev_close[col] = float(row[col])

        return pd.DataFrame(results).set_index("date")
