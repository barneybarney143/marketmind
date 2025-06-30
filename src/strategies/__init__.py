from __future__ import annotations

from .bollinger import BollingerStrategy
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
    "boll": BollingerStrategy,
    "rsi": RSIStrategy,
}

__all__ = [
    "BreakoutStrategy",
    "DualMomentumStrategy",
    "IBSStrategy",
    "MACDStrategy",
    "BollingerStrategy",
    "RSIStrategy",
    "STRATEGIES",
]
