from __future__ import annotations

from .breakout import BreakoutStrategy
from .ibs import IBSStrategy
from .macd import MACDStrategy
from .rsi import RSIStrategy

STRATEGIES = {
    "breakout": BreakoutStrategy,
    "ibs": IBSStrategy,
    "macd": MACDStrategy,
    "rsi": RSIStrategy,
}

__all__ = [
    "BreakoutStrategy",
    "IBSStrategy",
    "MACDStrategy",
    "RSIStrategy",
    "STRATEGIES",
]
