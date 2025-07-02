from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.hfea55 import HFEA55Strategy  # noqa: E402


def test_hfea55_rebalance() -> None:
    index = pd.date_range("2024-01-02", periods=6, freq="B")
    data = pd.DataFrame({"3USL": range(6), "3TYL": range(6)}, index=index)
    strat = HFEA55Strategy(rebalance_days=3)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert isinstance(signals[0], dict)
    assert isinstance(signals[3], dict)

