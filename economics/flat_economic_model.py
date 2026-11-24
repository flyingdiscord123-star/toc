"""Simple deterministic economic consequence model."""

from __future__ import annotations

from agents.action import AgentAction
from agents.observation import AgentObservation
from config.simulation_config import GovernanceConfig

from .economic_model import EconomicModel
from .economic_outcome import EconomicOutcome


class FlatEconomicModel(EconomicModel):
    """Return the candidate extraction income as economic outcome."""

    def evaluate(
        self,
        observation: AgentObservation,
        action: AgentAction,
        governance_config: GovernanceConfig,
    ) -> EconomicOutcome:
        """Return deterministic gross, cost, and net income values."""
        _ = observation
        gross_income = action.extraction_amount
        _ = governance_config
        return EconomicOutcome.create(gross_income=gross_income)
