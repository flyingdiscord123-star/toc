"""Interfaces for deterministic economic consequence models."""

from __future__ import annotations

from abc import ABC, abstractmethod

from agents.action import AgentAction
from agents.observation import AgentObservation
from config.simulation_config import GovernanceConfig

from .economic_outcome import EconomicOutcome


class EconomicModel(ABC):
    """Translate a candidate action into an economic outcome."""

    @abstractmethod
    def evaluate(
        self,
        observation: AgentObservation,
        action: AgentAction,
        governance_config: GovernanceConfig,
    ) -> EconomicOutcome:
        """Return the economic consequences of a candidate action."""
        raise NotImplementedError
