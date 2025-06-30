from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from scripts import backtest  # noqa: E402
from scripts import signal as signal_script
from strategies import STRATEGIES  # noqa: E402


class DummyDownloader:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def get_history(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        return self.data


def _patch_downloader(monkeypatch, module, data: pd.DataFrame) -> None:
    dummy = DummyDownloader(data)
    monkeypatch.setattr(module, "DataDownloader", lambda: dummy)


def _patch_strategy_loader(monkeypatch, module) -> None:
    def loader(name: str, params: dict[str, float] | None = None):
        params = params or {}
        cls = STRATEGIES[name]
        return cls(**params)

    monkeypatch.setattr(module, "load_strategy", loader)


def test_readme_backtest_example(monkeypatch, tmp_path, capsys) -> None:
    data = pd.DataFrame(
        {"close": range(1, 16)},
        index=pd.date_range("2020-01-01", periods=15),
    )
    _patch_downloader(monkeypatch, backtest, data)
    _patch_strategy_loader(monkeypatch, backtest)
    monkeypatch.chdir(tmp_path)
    argv = [
        "backtest.py",
        "--strategy",
        "rsi",
        "--ticker",
        "SPY",
        "--start",
        "2020-01-01",
        "--end",
        "2020-01-15",
        "--params",
        '{"rsi_buy": 30, "rsi_sell": 70}',
    ]
    monkeypatch.setattr(sys, "argv", argv)
    backtest.main()
    out = capsys.readouterr().out
    assert "strategy" in out
    assert "CAGR" in out


def test_readme_signal_example(monkeypatch, capsys) -> None:
    data = pd.DataFrame(
        {"close": range(1, 11)},
        index=pd.date_range("2020-01-01", periods=10),
    )
    _patch_downloader(monkeypatch, signal_script, data)
    _patch_strategy_loader(monkeypatch, signal_script)
    argv = [
        "signal.py",
        "--strategy",
        "rsi",
        "--ticker",
        "SPY",
        "--lookback",
        "10",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    signal_script.main()
    out = capsys.readouterr().out.strip()
    assert out in {"BUY", "SELL", "HOLD"}

