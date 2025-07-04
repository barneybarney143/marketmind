# metrics.py

Utility functions for evaluating back-test results.

- `cagr(equity, start, end)` – Compound Annual Growth Rate
- `sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252)`
- `max_drawdown(drawdown)` – minimum value of a drawdown series

All functions accept pandas series and return a float.
