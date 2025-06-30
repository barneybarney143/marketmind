from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from importlib import import_module
from pathlib import Path

from data import DataDownloader
from strategies.base import Strategy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def load_strategy(name: str) -> Strategy:
    module = import_module(f"strategies.{name}")
    cls = getattr(module, "Strategy")
    return cls()


def main() -> None:
    parser = argparse.ArgumentParser(description="Show latest trading signal")
    parser.add_argument("--strategy", required=True, help="Strategy module name")
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
    strategy = load_strategy(args.strategy)

    signal = "HOLD"
    for _, bar in data.iterrows():
        signal = strategy.next_bar(bar)

    print(signal)


if __name__ == "__main__":
    main()
