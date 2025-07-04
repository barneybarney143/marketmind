# fetch.py

CLI wrapper for `fetch_data.fetch()`.
Allows pulling historical prices for a comma-separated list of tickers and
optionally writing them to CSV files or printing JSON to stdout.

## Example

```bash
python fetch.py --tickers "SPY,IDTL" --start 2020-01-01 --end 2020-06-30 --csv-out data
```

### Options
- `--tickers` – comma separated symbols (required)
- `--start` / `--end` – ISO date range
- `--interval` – bar interval (passed through)
- `--ucits-off` – disable UCITS ticker mapping
- `--csv-out` – directory to write CSV files
- `--json` – print data as JSON on stdout
