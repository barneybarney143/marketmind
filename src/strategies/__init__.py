from __future__ import annotations

from .bollinger import BollingerStrategy
from .breakout import BreakoutStrategy
from .dual_mom import DualMomentumStrategy
from .ibs import IBSStrategy
from .macd import MACDStrategy
from .rsi import RSIStrategy
from .leveragedtrend import LeveragedTrendStrategy
from .hfea55 import HFEA55Strategy
from .covered_call_median import CoveredCallMedianStrategy
from .eom_bond import EndOfMonthBondPopStrategy

ALL_CLASSES = [
    BreakoutStrategy,
    DualMomentumStrategy,
    IBSStrategy,
    MACDStrategy,
    BollingerStrategy,
    RSIStrategy,
    LeveragedTrendStrategy,
    HFEA55Strategy,
    CoveredCallMedianStrategy,
    EndOfMonthBondPopStrategy,
]

STRATEGIES = {
    cls.__name__.replace("Strategy", "").lower(): cls for cls in ALL_CLASSES
}
if "dualmomentum" in STRATEGIES:
    STRATEGIES["dual_mom"] = STRATEGIES.pop("dualmomentum")

__all__ = [cls.__name__ for cls in ALL_CLASSES] + ["STRATEGIES"]
