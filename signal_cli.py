from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from data import DataDownloader  # noqa: E402
from strategies import STRATEGIES  # noqa: E402
from strategies.base import Strategy  # noqa: E402
from typing import cast  # noqa: E402

def load_strategy(name: str) -> Strategy:
    cls = STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy: {name}")
    return cast(type[Strategy], cls)()


def main() -> None:
    parser = argparse.ArgumentParser(description="Show latest trading signal")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--strategy", help="Strategy module name")
    group.add_argument("--all", action="store_true", help="Run all strategies")
    parser.add_argument("--ticker", required=True, help="Ticker symbol")
    parser.add_argument(
        "--lookback",
        type=int,
        default=365,
        help="Lookback period in days",
    )
    args = parser.parse_args()

    end = datetime.utcnow().date()
    start = end - timedelta(days=args.lookback)

    downloader = DataDownloader()
    data = downloader.get_history(args.ticker, str(start), str(end))

    strat_names: list[str]
    if args.all:
        strat_names = list(STRATEGIES.keys())
    else:
        assert args.strategy is not None
        strat_names = [args.strategy]

    for name in strat_names:
        try:
            strategy = load_strategy(name)
        except TypeError:
            print(f"{name}: N/A")
            continue
        signal_value: str | dict[str, float] = "HOLD"
        for _, bar in data.iterrows():
            signal_value = strategy.next_bar(bar)
        out = signal_value if isinstance(signal_value, str) else "N/A"
        print(f"{name}: {out}")


if __name__ == "__main__":
    main()
