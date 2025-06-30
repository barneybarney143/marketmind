from __future__ import annotations

from math import sqrt
from typing import Any

import pandas as pd


def cagr(
    equity: pd.Series[Any], start: str | pd.Timestamp, end: str | pd.Timestamp
) -> float:
    """Compute Compound Annual Growth Rate for *equity* between *start* and *end*."""
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    years = (end_ts - start_ts).days / 365.25
    if years == 0:
        return 0.0
    final_equity = float(equity.iloc[-1])
    return float(final_equity ** (1 / years) - 1)


def sharpe_ratio(
    returns: pd.Series[float], risk_free_rate: float = 0.0, periods_per_year: int = 252
) -> float:
    """Return annualized Sharpe ratio of *returns*."""
    if returns.empty:
        return 0.0
    excess = returns - risk_free_rate / periods_per_year
    std = float(excess.std(ddof=0))
    if std == 0:
        return 0.0
    mean = float(excess.mean())
    return mean / std * sqrt(periods_per_year)


def max_drawdown(drawdown: pd.Series[float]) -> float:
    """Return maximum drawdown from a drawdown series."""
    if drawdown.empty:
        return 0.0
    return float(drawdown.min())
