# Class Intent Reference

This document summarises the purpose of each class in the current code base. It can be used by AI agents when rewriting the framework from scratch.

## Core Utilities

### `DataDownloader`
Source: `src/data.py`

Downloads and caches historical OHLCV price data using **yfinance**. Normalises columns, fills missing required columns, and stores per-ticker parquet files in a cache directory.

### `Backtester`
Source: `src/engine.py`

Runs a simple long-only back-test over historical data. It feeds each bar into a strategy, executes buy/sell signals, maintains equity and drawdown, and records trades.

### `PromptEntry`
Source: `analyze_cognitive_load.py`

Dataclass for log entries produced by `track_prompt.py`. Captures timestamp, prompt complexity and quality for monitoring cognitive load.

## Strategy Base Classes

### `Strategy`
Source: `src/strategies/base.py`

Abstract base class for trading strategies. Provides parameter storage, position tracking and a `next_bar` interface that returns a signal string or weight mapping.

### `HistoryStrategy`
Source: `src/strategies/base.py`

Extends `Strategy` with a history of closing prices. Useful for strategies that require look-back calculations.

## Concrete Strategies

Classes below implement `next_bar` to produce trading signals.

- **`BreakoutStrategy`** (`src/strategies/breakout.py`)
  - Weekly 52‑week high breakout with trailing stop.
- **`BollingerStrategy`** (`src/strategies/bollinger.py`)
  - Mean reversion using weekly Bollinger Bands.
- **`DualMomentumStrategy`** (`src/strategies/dual_mom.py`)
  - Rotates into top‑performing ETFs on a monthly basis.
- **`IBSStrategy`** (`src/strategies/ibs.py`)
  - Trades based on Internal Bar Strength thresholds.
- **`MACDStrategy`** (`src/strategies/macd.py`)
  - Uses MACD crosses on weekly data to enter/exit.
- **`RSIStrategy`** (`src/strategies/rsi.py`)
  - Mean reversion using weekly RSI levels.
- **`LeveragedTrendStrategy`** (`src/strategies/leveragedtrend.py`)
  - Trend following on a leveraged S&P 500 ETF based on a moving average.
- **`HFEA55Strategy`** (`src/strategies/hfea55.py`)
  - Maintains a 55/45 leveraged stock/bond allocation rebalanced monthly.
- **`CoveredCallMedianStrategy`** (`src/strategies/median_cc.py`)
  - Buys or sells a covered‑call ETF when price deviates from its rolling median.
- **`EndOfMonthBondPopStrategy`** (`src/strategies/eom_bond.py`)
  - Holds a Treasury ETF only during the last few trading days of each month.

## Code Quality & Testing

- Linting via **Ruff** and static typing via **mypy**. Configuration in `pyproject.toml`.
- Unit tests live in `tests/` and are run with **pytest**. Coverage settings are also in `pyproject.toml`.
- Before committing, run `ruff check .`, `mypy` and `pytest -q` to ensure quality and test coverage.

