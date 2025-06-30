import pandas as pd

from engine import Backtester
from strategies.base import Strategy


class SequenceStrategy(Strategy):
    """Emit a predefined sequence of signals."""

    def __init__(self, signals: list[str]) -> None:
        super().__init__()
        self._signals = iter(signals)

    def next_bar(self, bar: pd.Series) -> str:  # type: ignore[override]
        return next(self._signals, "HOLD")


def test_backtester_multi_asset_switch() -> None:
    data = pd.DataFrame(
        {
            "AAA": [100, 101, 102],
            "BBB": [200, 201, 202],
        },
        index=pd.date_range("2024-01-01", periods=3, freq="D"),
    )
    strategy = SequenceStrategy(["BUY:AAA", "BUY:BBB", "SELL:BBB"])
    bt = Backtester(strategy, data)
    results = bt.run()

    # ensure trades are recorded for sell and buy switches
    assert bt.trades == [
        ("BUY", "AAA", pd.Timestamp("2024-01-01"), 100.0),
        ("SELL", "AAA", pd.Timestamp("2024-01-02"), 101.0),
        ("BUY", "BBB", pd.Timestamp("2024-01-02"), 201.0),
        ("SELL", "BBB", pd.Timestamp("2024-01-03"), 202.0),
    ]
    assert len(results) == len(data)


def test_backtester_single_asset_flow() -> None:
    data = pd.DataFrame(
        {"close": [10, 11, 12]}, index=pd.date_range("2024-01-01", periods=3, freq="D")
    )
    strategy = SequenceStrategy(["BUY", "SELL"])  # remaining bars HOLD
    bt = Backtester(strategy, data)
    bt.run()

    assert bt.trades == [
        ("BUY", "close", pd.Timestamp("2024-01-01"), 10.0),
        ("SELL", "close", pd.Timestamp("2024-01-02"), 11.0),
    ]
