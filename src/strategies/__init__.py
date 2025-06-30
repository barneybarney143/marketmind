from __future__ import annotations

from .breakout import BreakoutStrategy
from .dual_mom import DualMomentumStrategy
from .ibs import IBSStrategy
from .macd import MACDStrategy
from .rsi import RSIStrategy

STRATEGIES = {
    "breakout": BreakoutStrategy,
    "dual_mom": DualMomentumStrategy,
    "ibs": IBSStrategy,
    "macd": MACDStrategy,
    "rsi": RSIStrategy,
}

__all__ = [
    "BreakoutStrategy",
    "DualMomentumStrategy",
    "IBSStrategy",
    "MACDStrategy",
    "RSIStrategy",
    "STRATEGIES",
]
