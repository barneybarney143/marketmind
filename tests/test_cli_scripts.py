from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

import importlib.util  # noqa: E402

import backtest  # noqa: E402

signal_path = project_root / "signal.py"
spec = importlib.util.spec_from_file_location("signal_cli", signal_path)
assert spec and spec.loader
signal_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signal_cli)


def test_backtest_main(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_get_history(*args: str, **kwargs: str) -> pd.DataFrame:
        index = pd.date_range("2020-01-01", periods=3, freq="D")
        return pd.DataFrame({"close": [1.0, 1.1, 1.2]}, index=index)

    monkeypatch.setattr(backtest.DataDownloader, "get_history", fake_get_history)

    monkeypatch.chdir(tmp_path)

    argv = [
        "backtest.py",
        "--strategy",
        "rsi",
        "--ticker",
        "TEST",
        "--start",
        "2020-01-01",
        "--end",
        "2020-01-04",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    backtest.main()
    out = capsys.readouterr().out
    assert "strategy" in out.lower()

    result_file = tmp_path / "results" / "rsi_99914b93_TEST.csv"
    assert result_file.exists()


def test_signal_main(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_get_history(*args: str, **kwargs: str) -> pd.DataFrame:
        index = pd.date_range("2020-01-01", periods=5, freq="D")
        return pd.DataFrame(
            {
                "close": [1, 2, 3, 4, 5],
                "high": [2, 3, 4, 5, 6],
                "low": [1, 1, 2, 3, 4],
            },
            index=index,
        )

    monkeypatch.setattr(signal_cli.DataDownloader, "get_history", fake_get_history)

    argv = [
        "signal.py",
        "--strategy",
        "rsi",
        "--ticker",
        "TEST",
        "--lookback",
        "5",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    signal_cli.main()
    out = capsys.readouterr().out.strip()
    name, val = out.split(": ")
    assert name == "rsi"
    assert val in {"BUY", "SELL", "HOLD"}


def test_signal_main_all(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_get_history(*args: str, **kwargs: str) -> pd.DataFrame:
        index = pd.date_range("2020-01-01", periods=5, freq="D")
        return pd.DataFrame(
            {
                "close": [1, 2, 3, 4, 5],
                "high": [2, 3, 4, 5, 6],
                "low": [1, 1, 2, 3, 4],
            },
            index=index,
        )

    monkeypatch.setattr(signal_cli.DataDownloader, "get_history", fake_get_history)

    argv = [
        "signal.py",
        "--all",
        "--ticker",
        "TEST",
        "--lookback",
        "5",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    signal_cli.main()
    out_lines = capsys.readouterr().out.strip().splitlines()
    assert len(out_lines) == len(signal_cli.STRATEGIES)
    for line in out_lines:
        name, val = line.split(": ")
        assert name in signal_cli.STRATEGIES
        assert val in {"BUY", "SELL", "HOLD", "N/A"}

