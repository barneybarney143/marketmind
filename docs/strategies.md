# Strategies

## LeveragedTrendStrategy
Long the Xtrackers S&P 500 2× (ISIN LU0411078552) when the close is above its 200‑day simple moving average. Otherwise stay in cash. Parameter `sma_len` controls the SMA length in days.

## HFEA55Strategy
Allocates 55 % to WisdomTree S&P 500 3× (ISIN IE00B7KQZF44, ticker `3USL`) and 45 % to WisdomTree 10‑Yr Treasury 3× (ISIN IE00BKT09032, ticker `3TYL`). The portfolio is rebalanced at each month end. Parameter `rebalance_days` sets the minimum business days between rebalances.

## CoveredCallMedianStrategy
Trades the Global X S&P 500 Covered Call UCITS ETF (ISIN IE00BKT6Q882, ticker `XYLU`) using a 60‑day rolling median. Buy when price is below `(1 − band)` times the median and sell when above `(1 + band)` times the median. Parameter `band` is expressed as a percent.

## EndOfMonthBondPopStrategy
Holds the iShares $ Treasury 20+ yr UCITS ETF (ISIN IE00B1FZS806, ticker `IDTL`) only for the final `hold_days` trading days of each calendar month.
