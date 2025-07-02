from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from strategies.hfea55 import HFEA55Strategy  # noqa: E402


def test_hfea55_weights() -> None:
    index = pd.date_range("2024-01-02", periods=40, freq="B")
    data = pd.DataFrame({"3USL": 100.0, "3TYL": 100.0}, index=index)

    strat = HFEA55Strategy(rebalance_days=20)
    signals = [strat.next_bar(row) for _, row in data.iterrows()]

    assert any(isinstance(s, dict) and s for s in signals)
