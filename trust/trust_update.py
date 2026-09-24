"""
trust_update.py

Defines strategies for updating trust between agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class TrustUpdateStrategy(ABC):
    """
    Base class for trust update algorithms.
    """

    @abstractmethod
    def update(
        self,
        current_trust: float,
        successful_interaction: bool,
    ) -> float:
        """
        Return the updated trust value.
        """
        raise NotImplementedError


class LinearTrustUpdate(TrustUpdateStrategy):
    """
    Simple linear trust update.

    Successful interactions increase trust.
    Failed interactions decrease trust.
    """

    def __init__(
        self,
        increase: float = 0.05,
        decrease: float = 0.10,
    ) -> None:
        self._increase = increase
        self._decrease = decrease

    def update(
        self,
        current_trust: float,
        successful_interaction: bool,
    ) -> float:

        if successful_interaction:
            current_trust += self._increase
        else:
            current_trust -= self._decrease

        return max(0.0, min(1.0, current_trust))