"""Tests for single-parameter SVO gradient learning."""

from __future__ import annotations

import math
import unittest

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from config.simulation_config import (
    AgentConfig,
    EnvironmentConfig,
    GovernanceConfig,
    LearningAlgorithm,
    LearningConfig,
    NetworkConfig,
    NetworkTopology,
    SimulationConfig,
)
from economics.economic_outcome import EconomicOutcome
from environment.environment import EnvironmentSnapshot
from learning.experience import LearningExperience
from learning.factory import LearningFactory
from learning.gradient_utility import (
    GradientUtilityLearning,
    SVOGradientLearning,
)
from simulation import Simulation


class RecordingSVOGradientLearning(SVOGradientLearning):
    def __init__(self) -> None:
        super().__init__()
        self.last_experience: LearningExperience | None = None

    def update(self, experience: LearningExperience) -> None:
        self.last_experience = experience
        super().update(experience)


class SVOGradientLearningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.character = Character.cooperative()
        self.experience = LearningExperience(
            observation=AgentObservation(
                round_number=0,
                environment=EnvironmentSnapshot(
                    round_number=0,
                    available_resources=80.0,
                    maximum_capacity=100.0,
                    regeneration_rate=5.0,
                ),
            ),
            chosen_action=AgentAction(extraction_amount=4.0),
            economic_outcome=EconomicOutcome(
                gross_income=8.0,
                tax_paid=0.0,
                net_income=8.0,
            ),
            utility_component_scores=(
                ("wealth", 0.2),
                ("sustainability", 0.7),
            ),
            total_utility=0.5,
            character=self.character,
            chosen_w=0.2,
            chosen_s=0.7,
            predicted_utility=0.5,
            realized_reward=8.0,
            normalization_capacity=100.0,
        )

    def test_alias_and_learning_config_defaults(self) -> None:
        self.assertIs(GradientUtilityLearning, SVOGradientLearning)
        config = LearningConfig()
        self.assertEqual(config.learning_rate, 0.01)
        self.assertEqual(config.anchor_lambda, 0.20)

    def test_updates_theta_with_exact_gradient_and_baseline_anchor(self) -> None:
        learner = SVOGradientLearning(
            learning_rate=0.01,
            anchor_lambda=0.20,
        )
        theta = self.character.theta
        td_error = 8.0 / 100.0 - 0.5
        gradient = (
            -math.sin(theta) * 0.2
            + math.cos(theta) * 0.7
        )
        clamped = min(
            max(theta + 0.01 * td_error * gradient, 0.0),
            math.pi / 2,
        )
        expected = 0.8 * clamped + 0.2 * self.character.initial_theta

        learner.update(self.experience)

        self.assertAlmostEqual(self.character.theta, expected)
        self.assertEqual(self.character.initial_theta, math.radians(64.0))

    def test_angle_update_is_clamped_to_valid_range(self) -> None:
        character = Character.risk_averse()
        experience = LearningExperience(
            observation=self.experience.observation,
            chosen_action=self.experience.chosen_action,
            economic_outcome=self.experience.economic_outcome,
            utility_component_scores=self.experience.utility_component_scores,
            total_utility=1.0,
            character=character,
            chosen_w=1.0,
            chosen_s=0.0,
            predicted_utility=1.0,
            realized_reward=0.0,
            normalization_capacity=100.0,
        )
        SVOGradientLearning(
            learning_rate=100.0,
            anchor_lambda=0.0,
        ).update(experience)
        self.assertEqual(character.theta, math.pi / 2)

    def test_factory_builds_configured_svo_learner(self) -> None:
        learner = LearningFactory.create(
            LearningAlgorithm.SVO_GRADIENT.value,
            learning_rate=0.03,
            anchor_lambda=0.4,
        )
        self.assertIsInstance(learner, SVOGradientLearning)
        self.assertEqual(learner.learning_rate, 0.03)
        self.assertEqual(learner.anchor_lambda, 0.4)

    def test_simulation_passes_chosen_components_and_reward_to_learner(self) -> None:
        config = SimulationConfig(
            environment=EnvironmentConfig(100.0, 100.0, 2.0, 1),
            network=NetworkConfig(
                topology=NetworkTopology.COMPLETE,
                random_seed=2,
            ),
            agents=AgentConfig(1, 0.0, 100.0, 0.0),
            governance=GovernanceConfig(quota_limit=5.0),
            learning=LearningConfig(
                learning_algorithm=LearningAlgorithm.SVO_GRADIENT,
            ),
        )
        simulation = Simulation(config)
        simulation.initialize()
        agent = simulation._agents[0]
        initial_theta = agent.theta
        learner = RecordingSVOGradientLearning()
        agent._learning = learner

        simulation.run()

        self.assertNotEqual(agent.theta, initial_theta)
        experience = learner.last_experience
        self.assertIsNotNone(experience)
        assert experience is not None
        extraction = experience.chosen_action.extraction_amount
        expected_w = (min(extraction, 100.0) / 100.0) ** 0.92
        post_extraction_stock = max(0.0, 100.0 - extraction)
        projected_stock = min(
            100.0,
            post_extraction_stock * (1.0 + 2.0 / 100.0),
        )
        expected_s = (projected_stock / 100.0) ** 0.85
        self.assertAlmostEqual(experience.chosen_w, expected_w)
        self.assertAlmostEqual(experience.chosen_s, expected_s)
        self.assertEqual(
            experience.utility_component_scores,
            (
                ("wealth", experience.chosen_w),
                ("sustainability", experience.chosen_s),
            ),
        )


if __name__ == "__main__":
    unittest.main()
