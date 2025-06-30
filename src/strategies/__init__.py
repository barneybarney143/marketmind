from __future__ import annotations

from .ibs import IBSStrategy
from .macd import MACDStrategy
from .rsi import RSIStrategy

STRATEGIES = {
    "ibs": IBSStrategy,
    "macd": MACDStrategy,
    "rsi": RSIStrategy,
}

__all__ = ["IBSStrategy", "MACDStrategy", "RSIStrategy", "STRATEGIES"]
