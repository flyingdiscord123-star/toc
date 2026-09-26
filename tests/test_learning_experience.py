"""Focused tests for the learning experience contract."""

from __future__ import annotations

import unittest
from uuid import uuid4

from agents.action import AgentAction
from agents.observation import AgentObservation
from economics.economic_outcome import EconomicOutcome
from environment.environment import EnvironmentSnapshot
from learning.experience import LearningExperience
from learning.no_learning import NoLearning


class LearningExperienceTests(unittest.TestCase):
    def setUp(self) -> None:
        observation = AgentObservation(
            round_number=0,
            environment=EnvironmentSnapshot(
                round_number=0,
                available_resources=100.0,
                maximum_capacity=100.0,
                regeneration_rate=2.0,
            ),
        )
        self.experience = LearningExperience(
            observation=observation,
            chosen_action=AgentAction(extraction_amount=10.0),
            economic_outcome=EconomicOutcome(
                gross_income=10.0,
                tax_paid=0.0,
                net_income=10.0,
            ),
            utility_component_scores=(("wealth", 1.0),),
            total_utility=1.0,
        )

    def test_is_immutable(self) -> None:
        with self.assertRaises(AttributeError):
            self.experience.total_utility = 0.0  # type: ignore[misc]

    def test_no_learning_accepts_update(self) -> None:
        NoLearning().update(self.experience)


if __name__ == "__main__":
    unittest.main()
