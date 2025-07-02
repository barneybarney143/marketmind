from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path
from typing import Any, cast

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from data import DataDownloader
from engine import Backtester
from metrics import cagr, max_drawdown
from strategies import STRATEGIES
from strategies.base import Strategy


def generate_param_grid(params: dict[str, Any]) -> list[dict[str, Any]]:
    """Return cartesian product of parameter values.

    Any value that is a list will be expanded. Single values are kept as-is.
    """
    keys = list(params)
    values = [v if isinstance(v, list) else [v] for v in params.values()]
    return [dict(zip(keys, combo)) for combo in itertools.product(*values)]


def load_strategy(name: str, params: dict[str, float]) -> Strategy:
    cls = STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy: {name}")
    return cast(type[Strategy], cls)(**params)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a strategy back-test")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--strategy", help="Strategy module name")
    group.add_argument("--all", action="store_true", help="Run all strategies")
    parser.add_argument("--ticker", required=True, help="Ticker symbol")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--params", default="{}", help="JSON encoded parameters")
    parser.add_argument("--sweep", action="store_true", help="Run parameter sweep")
    args = parser.parse_args()

    base_params: dict[str, Any] = json.loads(args.params)

    default_grids: dict[str, dict[str, list[float]]] = {
        "leveragedtrend": {"sma_len": [150, 200, 250]},
        "hfea55": {"rebalance_days": [20, 21, 22]},
        "median_cc": {"band": [0.005, 0.01, 0.015]},
        "eom_bond": {"hold_days": [5, 7, 9]},
    }

    strategies: list[str]
    if args.all:
        strategies = list(STRATEGIES.keys())
    else:
        strategies = [args.strategy]

    summary: list[tuple[str, str, float, float]] = []
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    for strat_name in strategies:
        params_for_strat = base_params or (
            default_grids.get(strat_name, {}) if args.sweep else {}
        )
        param_sets = (
            generate_param_grid(params_for_strat)
            if args.sweep
            else [params_for_strat]
        )
        for params in param_sets:
            strategy = load_strategy(strat_name, params)
            downloader = DataDownloader()
            data = downloader.get_history(args.ticker, args.start, args.end)
            backtester = Backtester(strategy, data)
            results = backtester.run()

            cagr_value = cagr(results["equity"], args.start, args.end)
            max_dd = max_drawdown(results["drawdown"])

            paramhash = hashlib.md5(
                json.dumps(params, sort_keys=True).encode()
            ).hexdigest()[:8]
            out_file = results_dir / f"{strat_name}_{paramhash}_{args.ticker}.csv"
            results.to_csv(out_file)
            summary.append((strat_name, paramhash, cagr_value, max_dd))

    print("strategy  params    CAGR     MaxDD")
    for strat, phash, cg, dd in summary:
        print(f"{strat:<8} {phash:<8} {cg:>7.2%} {dd:>9.2%}")


if __name__ == "__main__":
    main()
