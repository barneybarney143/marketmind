import sys
from types import ModuleType, SimpleNamespace
from pathlib import Path
from datetime import datetime, timedelta, date

import pandas as pd
import pytest

import analyze_cognitive_load as acl
import fetch_data
import track_prompt

# Provide lightweight stubs for optional third-party dependencies so that the
# tests can run without the real packages installed.
if "streamlit" not in sys.modules:
    stubs = ModuleType("streamlit")

    def cache_data(func=None, **kwargs):
        def decorator(f):
            return f

        return decorator(func) if callable(func) else decorator

    stubs.cache_data = cache_data
    stubs.sidebar = SimpleNamespace()
    sys.modules["streamlit"] = stubs

if "plotly" not in sys.modules:
    plotly_stub = ModuleType("plotly")
    go_stub = ModuleType("plotly.graph_objects")

    class Figure:  # minimal stand-in for plotly.graph_objects.Figure
        def __init__(self, *args, **kwargs):
            pass

    class Scatter:  # minimal stand-in for plotly.graph_objects.Scatter
        def __init__(self, *args, **kwargs):
            pass

    go_stub.Figure = Figure
    go_stub.Scatter = Scatter
    plotly_stub.graph_objects = go_stub
    sys.modules["plotly"] = plotly_stub
    sys.modules["plotly.graph_objects"] = go_stub

import streamlit_app


# ---------- analyze_cognitive_load tests ----------

def test_parse_logs_and_load_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    log_file = tmp_path / "log.md"
    log_file.write_text(
        "\n".join([
            "## 2030-01-01T00:00",
            "complexity_score: 0.5",
            "quality: high",
            "## 2030-01-01T01:00",
            "complexity_score: 0.8",
            "quality: low",
        ])
    )
    cfg_file = tmp_path / "tracker_config.yaml"
    cfg_file.write_text("max_prompts_hour: 1")
    monkeypatch.setattr(acl, "CONFIG_PATH", cfg_file)
    entries = acl.parse_logs(log_file)
    assert len(entries) == 2
    assert entries[0].complexity == 0.5
    assert entries[1].quality == "low"
    cfg = acl.load_config()
    assert cfg["max_prompts_hour"] == 1


def test_analyze_and_main_overload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    now = datetime.utcnow()
    entries = [
        acl.PromptEntry(now - timedelta(minutes=i), 0.9, "low") for i in range(3)
    ]
    cfg = {
        "max_prompts_hour": 2,
        "max_complexity_avg_hour": 0.1,
        "max_active_hours_day": 0.01,
        "complex_threshold": 0.8,
    }
    assert acl.analyze(entries, cfg) is True
    log_file = tmp_path / "log.md"
    with log_file.open("w") as f:
        for e in entries:
            f.write(
                "## {ts}\ncomplexity_score: {c}\nquality: {q}\n".format(
                    ts=e.timestamp.isoformat(),
                    c=e.complexity,
                    q=e.quality,
                )
            )
    cfg_file = tmp_path / "tracker_config.yaml"
    cfg_file.write_text("max_prompts_hour: 2")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(acl, "CONFIG_PATH", cfg_file)
    monkeypatch.setattr(sys, "argv", ["prog", str(log_file)])
    with pytest.raises(SystemExit):
        acl.main()
    assert (tmp_path / ".you-need-a-break").exists()


# ---------- fetch_data tests ----------

def _fake_history(*args: str, **kwargs: str) -> pd.DataFrame:
    idx = pd.date_range("2020-01-01", periods=2, freq="D")
    return pd.DataFrame(
        {
            "open": [1, 2],
            "high": [2, 3],
            "low": [1, 1],
            "close": [1, 2],
            "adj_close": [1, 2],
            "volume": [10, 20],
        },
        index=idx,
    )


def test_fetch_data_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(fetch_data.DataDownloader, "get_history", _fake_history)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["fetch_data.py", "SPY", "IDTL"])
    fetch_data._main()
    out = capsys.readouterr().out
    assert "Wrote SPY.csv" in out
    assert Path("SPY.csv").exists()
    assert Path("IDTL.csv").exists()


def test_fetch_data_main_usage(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["fetch_data.py"])
    with pytest.raises(SystemExit):
        fetch_data._main()
    assert "Usage" in capsys.readouterr().out


# ---------- track_prompt utilities ----------

def test_track_prompt_utils(tmp_path: Path) -> None:
    long_text = "word " * 30
    short = track_prompt.shorten_prompt(long_text, max_len=20)
    assert len(short) <= 20
    assert track_prompt.estimate_tokens("four words") == 2
    score = track_prompt.compute_readability("Simple sentence.")
    assert isinstance(score, float)
    assert track_prompt.quality_from_readability(70) == "high"
    assert track_prompt.quality_from_readability(50) == "medium"
    assert track_prompt.quality_from_readability(10) == "low"
    log = tmp_path / "log.md"
    track_prompt.append_log(log, datetime(2030, 1, 1), {"a": 1})
    assert log.exists()
    content = log.read_text()
    assert "a: 1" in content


# ---------- streamlit_app tests ----------

def _setup_streamlit(monkeypatch: pytest.MonkeyPatch):
    import streamlit_app as sa

    class DummySidebar:
        def __init__(self):
            self.buttons: dict[str, bool] = {}
        def selectbox(self, *args, **kwargs):
            return "DummyStrategy"
        def text_input(self, *args, **kwargs):
            return "SPY"
        def date_input(self, *args, **kwargs):
            return date(2020, 1, 1)
        def button(self, name: str):
            return self.buttons.get(name, False)
        def expander(self, *args, **kwargs):
            class Ctx:
                def __enter__(self):
                    return None
                def __exit__(self, *exc):
                    return False
            return Ctx()

    class DummySt:
        def __init__(self):
            self.sidebar = DummySidebar()
            self.record: dict[str, object] = {}
        def checkbox(self, *args, **kwargs):
            return False
        def number_input(self, *args, **kwargs):
            return 1
        def text_input(self, *args, **kwargs):
            return "x,y"
        def plotly_chart(self, *args, **kwargs):
            self.record["plot"] = True
        def table(self, df):
            self.record["table"] = df
        def error(self, msg):
            self.record["error"] = msg
        def markdown(self, text, **kwargs):
            self.record["markdown"] = text

    dummy = DummySt()
    monkeypatch.setattr(sa, "st", dummy)
    return dummy


def test_streamlit_app_functions(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy_st = _setup_streamlit(monkeypatch)
    idx = pd.date_range("2020-01-01", periods=2, freq="D")
    df = pd.DataFrame({"close": [1, 2]}, index=idx)
    monkeypatch.setattr(streamlit_app.DataDownloader, "get_history", lambda *a, **k: df)

    class FakeBacktester:
        def __init__(self, *a, **k):
            pass
        def run(self):
            return pd.DataFrame({"equity": [1, 2], "drawdown": [0, -0.1]}, index=idx)

    monkeypatch.setattr(streamlit_app, "Backtester", FakeBacktester)
    monkeypatch.setattr(streamlit_app, "cagr", lambda *a, **k: 0.1)
    monkeypatch.setattr(streamlit_app, "max_drawdown", lambda *a, **k: -0.1)
    monkeypatch.setattr(streamlit_app, "sharpe_ratio", lambda *a, **k: 1.0)

    from typing import Iterable

    class DummyStrategy:
        def __init__(
            self, a: int = 1, flag: bool = False, items: Iterable[str] | None = None
        ) -> None:
            self.params = (a, flag, items)

        def next_bar(self, row: pd.Series) -> str:
            return "BUY"

    params = streamlit_app.get_param_inputs(DummyStrategy)
    assert params == {"a": 1.0, "flag": False, "items": ["x", "y"]}

    streamlit_app.run_backtest(
        DummyStrategy,
        "SPY",
        "2020-01-01",
        "2020-01-02",
        {},
    )
    assert dummy_st.record.get("plot")
    assert "CAGR" in dummy_st.record["table"].columns

    streamlit_app.latest_signal(
        DummyStrategy,
        "SPY",
        "2020-01-01",
        "2020-01-02",
        {},
    )
    assert "BUY" in dummy_st.record["markdown"]

    monkeypatch.setattr(
        streamlit_app.strategies,
        "STRATEGIES",
        {"dummy": DummyStrategy},
    )
    monkeypatch.setattr(
        streamlit_app.strategies,
        "DummyStrategy",
        DummyStrategy,
        raising=False,
    )
    streamlit_app.all_latest_signals("SPY", "2020-01-01", "2020-01-02")
    assert not dummy_st.record.get("error")

    # error paths
    def fail(*args: object, **kwargs: object) -> None:
        raise Exception("fail")

    monkeypatch.setattr(streamlit_app, "load_data", fail)
    dummy_st.record.clear()
    streamlit_app.run_backtest(DummyStrategy, "SPY", "2020-01-01", "2020-01-02", {})
    assert "error" in dummy_st.record
    dummy_st.record.clear()
    streamlit_app.latest_signal(DummyStrategy, "SPY", "2020-01-01", "2020-01-02", {})
    assert "error" in dummy_st.record
    dummy_st.record.clear()
    streamlit_app.all_latest_signals("SPY", "2020-01-01", "2020-01-02")
    assert "error" in dummy_st.record

    # Test main calling run_backtest via sidebar button
    # main buttons
    def rec_latest(*args: object, **kwargs: object) -> None:
        dummy_st.record.setdefault("latest", True)

    def rec_all(*args: object, **kwargs: object) -> None:
        dummy_st.record.setdefault("all", True)

    monkeypatch.setattr(streamlit_app, "latest_signal", rec_latest)
    monkeypatch.setattr(streamlit_app, "all_latest_signals", rec_all)
    monkeypatch.setattr(
        streamlit_app.strategies,
        "__all__",
        ["DummyStrategy", "STRATEGIES"],
    )
    monkeypatch.setattr(
        streamlit_app.strategies,
        "DummyStrategy",
        DummyStrategy,
        raising=False,
    )
    # Run backtest button
    dummy_st.sidebar.buttons = {"Run Back-test": True}
    def rec_run(*args: object, **kwargs: object) -> None:
        dummy_st.record.setdefault("ran", True)

    monkeypatch.setattr(streamlit_app, "run_backtest", rec_run)
    streamlit_app.main()
    assert dummy_st.record.get("ran")
    # Latest Signal button
    dummy_st.sidebar.buttons = {"Latest Signal": True}
    streamlit_app.main()
    assert dummy_st.record.get("latest")
    # All Strategy Signals button
    dummy_st.sidebar.buttons = {"All Strategy Signals": True}
    streamlit_app.main()
    assert dummy_st.record.get("all")
