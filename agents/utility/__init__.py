"""Modular utility interfaces and implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility_weights import UtilityWeights


class UtilityFunction(ABC):
    """Interface for evaluating candidate actions."""

    @abstractmethod
    def evaluate(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> float:
        """Return the utility of a candidate action."""
        raise NotImplementedError


class PlaceholderUtilityFunction(UtilityFunction):
    """Utility function placeholder for future experiments."""

    def evaluate(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> float:
        """Signal that placeholder utility is not implemented."""
        _ = observation, action, state, character
        raise NotImplementedError(
            "Utility functions will be implemented in a future chapter."
        )


from .aggregator import LinearUtilityFunction


class SimpleUtilityFunction(LinearUtilityFunction):
    """Backward-compatible name for the linear utility function."""


from .component import UtilityComponent
from .compliance import ComplianceComponent
from .context import UtilityContext
from .risk import RiskComponent
from .report import UtilityEvaluation
from .sustainability import SustainabilityComponent
from .trust import TrustComponent
from .wealth import WealthComponent

__all__ = [
    "ComplianceComponent",
    "LinearUtilityFunction",
    "PlaceholderUtilityFunction",
    "RiskComponent",
    "SimpleUtilityFunction",
    "SustainabilityComponent",
    "TrustComponent",
    "UtilityEvaluation",
    "UtilityContext",
    "UtilityComponent",
    "UtilityFunction",
    "WealthComponent",
]
