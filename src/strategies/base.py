from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class Strategy(ABC):
    """Base class for trading strategies."""

    def __init__(self, **params: Any) -> None:
        self.params = params
        self.reset()

    def reset(self) -> None:
        """Reset internal state for a new back-test."""
        self.position = 0
        self.today: pd.Timestamp | None = None

    @abstractmethod
    def next_bar(self, bar: pd.Series[Any]) -> str:
        """Process the next market bar and return a trading signal."""
        raise NotImplementedError
