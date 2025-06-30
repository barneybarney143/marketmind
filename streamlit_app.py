from __future__ import annotations

import inspect
import sys
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import strategies
from data import DataDownloader
from engine import Backtester
from metrics import cagr, max_drawdown, sharpe_ratio


@st.cache_data
def load_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    downloader = DataDownloader()
    return downloader.get_history(ticker, start, end)


def get_param_inputs(strategy_cls: type[Any]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    with st.sidebar.expander("Parameters", expanded=False):
        sig = inspect.signature(strategy_cls.__init__)
        for name, param in list(sig.parameters.items())[1:]:
            default = param.default if param.default is not inspect._empty else ""
            ann = param.annotation
            if ann is bool or isinstance(default, bool):
                params[name] = st.checkbox(name, value=bool(default))
            elif ann in (int, float) or isinstance(default, (int, float)):
                params[name] = st.number_input(name, value=float(default))
            else:
                val = st.text_input(name, value=str(default))
                if "Iterable" in str(ann):
                    params[name] = [t.strip() for t in val.split(",") if t.strip()]
                else:
                    params[name] = val
    return params


def run_backtest(
    strategy_cls: type[Any],
    ticker: str,
    start: str,
    end: str,
    params: dict[str, Any],
) -> None:
    try:
        data = load_data(ticker, start, end)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Data download failed: {exc}")
        return

    strategy = strategy_cls(**params)
    bt = Backtester(strategy, data)
    results = bt.run()

    rets = results["equity"].pct_change().dropna()
    metrics = {
        "CAGR": cagr(results["equity"], start, end),
        "Max DD": max_drawdown(results["drawdown"]),
        "Sharpe": sharpe_ratio(rets),
    }

    fig = go.Figure(go.Scatter(x=results.index, y=results["equity"], name="Equity"))
    st.plotly_chart(fig, use_container_width=True)
    metrics_df = pd.DataFrame([metrics])
    metrics_df = metrics_df.style.format(
        {"CAGR": "{:.2%}", "Max DD": "{:.2%}", "Sharpe": "{:.2f}"}
    )
    st.table(metrics_df)


def latest_signal(
    strategy_cls: type[Any],
    ticker: str,
    start: str,
    end: str,
    params: dict[str, Any],
) -> None:
    try:
        data = load_data(ticker, start, end)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Data download failed: {exc}")
        return

    strat = strategy_cls(**params)
    signal = "HOLD"
    for _, row in data.iterrows():
        signal = strat.next_bar(row)

    color = {"BUY": "green", "SELL": "red", "HOLD": "gray"}.get(signal, "gray")
    badge = (
        f"<div style='font-size:48px;color:white;background-color:{color};"
        f"padding:0.2em;text-align:center'>{signal}</div>"
    )
    st.markdown(badge, unsafe_allow_html=True)


def main() -> None:
    strat_names = [n for n in strategies.__all__ if n != "STRATEGIES"]
    strat_name = st.sidebar.selectbox("Strategy", strat_names)
    ticker = st.sidebar.text_input("Ticker", value="SPY")
    start = st.sidebar.date_input("Start", value=date(2020, 1, 1))
    end = st.sidebar.date_input("End", value=date.today())

    strategy_cls = getattr(strategies, strat_name)
    params = get_param_inputs(strategy_cls)

    if st.sidebar.button("Run Back-test"):
        run_backtest(strategy_cls, ticker, str(start), str(end), params)
    if st.sidebar.button("Latest Signal"):
        latest_signal(strategy_cls, ticker, str(start), str(end), params)


if __name__ == "__main__":
    main()
