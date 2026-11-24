"""Focused tests for the deterministic economic model."""

from __future__ import annotations

import unittest

from agents.action import AgentAction
from agents.observation import AgentObservation
from config.simulation_config import GovernanceConfig
from economics import EconomicOutcome, FlatEconomicModel
from environment.environment import EnvironmentSnapshot


class FlatEconomicModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.observation = AgentObservation(
            round_number=0,
            environment=EnvironmentSnapshot(
                round_number=0,
                available_resources=100.0,
                maximum_capacity=100.0,
                regeneration_rate=2.0,
            ),
        )
        self.action = AgentAction(extraction_amount=10.0)

    def test_disabled_costs_preserve_gross_income(self) -> None:
        outcome = FlatEconomicModel().evaluate(
            observation=self.observation,
            action=self.action,
            governance_config=GovernanceConfig(),
        )

        self.assertEqual(
            outcome,
            EconomicOutcome(
                gross_income=10.0,
                net_income=10.0,
            ),
        )


if __name__ == "__main__":
    unittest.main()
