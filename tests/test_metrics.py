from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metrics import cagr, max_drawdown, sharpe_ratio  # noqa: E402


def test_cagr_basic() -> None:
    equity = pd.Series([1.0, 16.0])
    start = "2020-01-01"
    end = "2022-01-01"
    rate = cagr(equity, start, end)
    years = (pd.Timestamp(end) - pd.Timestamp(start)).days / 365.25
    expected = 16.0 ** (1 / years) - 1
    assert rate == pytest.approx(expected)


def test_cagr_zero_years() -> None:
    assert cagr(pd.Series([1.0]), "2020-01-01", "2020-01-01") == 0.0


def test_sharpe_ratio_basic() -> None:
    rets = pd.Series([0.1, 0.2, -0.1])
    ratio = sharpe_ratio(rets)
    assert ratio > 0


def test_sharpe_ratio_edge_cases() -> None:
    assert sharpe_ratio(pd.Series(dtype=float)) == 0.0
    assert sharpe_ratio(pd.Series([0.05, 0.05])) == 0.0


def test_max_drawdown() -> None:
    drawdown = pd.Series([0.0, -0.1, -0.05])
    assert max_drawdown(drawdown) == -0.1
    assert max_drawdown(pd.Series(dtype=float)) == 0.0
