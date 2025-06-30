from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from importlib import import_module
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data import DataDownloader
from engine import Backtester
from strategies.base import Strategy


def load_strategy(name: str, params: dict[str, float]) -> Strategy:
    module = import_module(f"strategies.{name}")
    cls = getattr(module, "Strategy")
    return cls(**params)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a strategy back-test")
    parser.add_argument("--strategy", required=True, help="Strategy module name")
    parser.add_argument("--ticker", required=True, help="Ticker symbol")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--params", default="{}", help="JSON encoded parameters")
    args = parser.parse_args()

    params = json.loads(args.params)

    strategy = load_strategy(args.strategy, params)
    downloader = DataDownloader()
    data = downloader.get_history(args.ticker, args.start, args.end)

    backtester = Backtester(strategy, data)
    results = backtester.run()

    duration_years = (
        datetime.fromisoformat(args.end) - datetime.fromisoformat(args.start)
    ).days / 365.25
    cagr = results["equity"].iloc[-1] ** (1 / duration_years) - 1
    print(f"CAGR: {cagr:.2%}")
    print(f"Final equity: {results['equity'].iloc[-1]:.2f}")


if __name__ == "__main__":
    main()
