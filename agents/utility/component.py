"""Interfaces for modular utility components."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .context import UtilityContext

MAXIMUM_CANDIDATE_EXTRACTION = 10.0


class UtilityComponent(ABC):
    """Evaluate one dimension of an agent's utility."""

    @abstractmethod
    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return the component score for a candidate action."""
        raise NotImplementedError
