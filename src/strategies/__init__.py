from __future__ import annotations

from .ibs import IBSStrategy

STRATEGIES = {
    "ibs": IBSStrategy,
}

__all__ = ["IBSStrategy", "STRATEGIES"]
