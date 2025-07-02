from __future__ import annotations

from .bollinger import BollingerStrategy
from .breakout import BreakoutStrategy
from .dual_mom import DualMomentumStrategy
from .ibs import IBSStrategy
from .macd import MACDStrategy
from .rsi import RSIStrategy
from .leveragedtrend import LeveragedTrendStrategy
from .hfea55 import HFEA55Strategy
from .median_cc import CoveredCallMedianStrategy
from .eom_bond import EndOfMonthBondPopStrategy

_classes = [
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
    cls.__name__.removesuffix("Strategy").lower(): cls for cls in _classes
}

__all__ = [cls.__name__ for cls in _classes] + ["STRATEGIES"]
