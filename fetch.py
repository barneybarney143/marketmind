from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fetch_data import fetch  # noqa: E402


def main() -> dict[str, pd.DataFrame]:
    parser = argparse.ArgumentParser(description="Fetch historical data")
    parser.add_argument("--tickers", required=True, help="Comma separated tickers")
    parser.add_argument("--start", default="2000-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    parser.add_argument("--interval", default="1d", help="Bar interval")
    parser.add_argument(
        "--ucits-off",
        action="store_true",
        help="Disable UCITS mapping",
    )
    parser.add_argument("--csv-out", help="Directory to write CSV files")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")
    args = parser.parse_args()

    ticker_list = [t.strip() for t in args.tickers.split(",") if t.strip()]

    data = fetch(
        ticker_list,
        start=args.start,
        end=args.end,
        interval=args.interval,
        ucits_map=not args.ucits_off,
    )

    if args.csv_out:
        out_dir = Path(args.csv_out)
        out_dir.mkdir(parents=True, exist_ok=True)
        for ticker, df in data.items():
            df.to_csv(out_dir / f"{ticker}.csv")

    if args.json:
        serialised = {
            t: df.reset_index()
            .assign(date=lambda d: d["date"].astype(str))
            .to_dict(orient="records")
            for t, df in data.items()
        }
        print(json.dumps(serialised))

    return data


if __name__ == "__main__":
    main()
