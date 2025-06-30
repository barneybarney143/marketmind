from __future__ import annotations

from .ibs import IBSStrategy
from .rsi import RSIStrategy

STRATEGIES = {
    "ibs": IBSStrategy,
    "rsi": RSIStrategy,
}

__all__ = ["IBSStrategy", "RSIStrategy", "STRATEGIES"]
