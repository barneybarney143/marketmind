# EU-friendly Reddit strategies

## LeveragedTrendStrategy (LU0411078552)

Long Xtrackers S&P 500 2× (ticker `XSP2`) when the weekly close is above its
`sma_len`-period simple moving average. Moves to cash when the close falls below
the SMA.

Parameters:
- `sma_len`: length of the moving average in trading days.

## HFEA55Strategy (IE00BMYDM794 / IE00BMYDRH76)

Maintains a monthly rebalanced portfolio of 55 % in the 3× S&P 500 ETF `3USL`
and 45 % in the 3× 10‑year Treasury ETF `3TYL`.

Parameters:
- `rebalance_days`: trading days between rebalances.

## CoveredCallMedianStrategy (IE00BYQYYS58)

Trades the Global X S&P 500 Covered Call UCITS ETF `XYLU` around its rolling
`window`‑day median. A buy occurs when price drops below `median × (1 − band)`;
a sell occurs when price rises above `median × (1 + band)`.

Parameters:
- `band`: percentage threshold around the median.
- `window`: lookback period for the median.

## EndOfMonthBondPopStrategy (IE00B14X4T88)

Holds the iShares $ Treasury 20+ year UCITS ETF `IDTL` for the last
`hold_days` trading days of each calendar month and stays in cash otherwise.

Parameters:
- `hold_days`: number of trading days to hold at month end.

