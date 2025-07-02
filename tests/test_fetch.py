from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

import fetch_data  # noqa: E402
import fetch as fetch_cli  # noqa: E402


def _fake_history(*args: str, **kwargs: str) -> pd.DataFrame:
    index = pd.date_range("2020-01-01", periods=2, freq="D")
    index.name = "date"
    return pd.DataFrame(
        {
            "open": [1, 2],
            "high": [2, 3],
            "low": [1, 1],
            "close": [1, 2],
            "adj_close": [1, 2],
            "volume": [10, 20],
        },
        index=index,
    )


def test_fetch_function(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fetch_data.DataDownloader, "get_history", _fake_history)
    result = fetch_data.fetch(["SPY", "IDTL"], start="2020-01-01", end="2020-01-02")
    assert set(result.keys()) == {"SPY", "IDTL"}
    for df in result.values():
        assert list(df.columns) == [
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]


def test_cli_writes_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fetch_data.DataDownloader, "get_history", _fake_history)

    argv = [
        "fetch.py",
        "--tickers",
        "SPY,IDTL",
        "--start",
        "2020-01-01",
        "--end",
        "2020-01-02",
        "--csv-out",
        str(tmp_path),
        "--json",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    data = fetch_cli.main()
    assert set(data.keys()) == {"SPY", "IDTL"}
    assert (tmp_path / "SPY.csv").exists()
    assert (tmp_path / "IDTL.csv").exists()
