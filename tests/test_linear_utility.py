"""Tests for the pure two-component SVO utility function."""

from __future__ import annotations

import math
import unittest
from uuid import uuid4

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility import (
    LinearUtilityFunction,
    SVOUtilityFunction,
    UtilityFunction,
)
from config.simulation_config import CharacterType
from environment.environment import EnvironmentSnapshot


class SVOUtilityFunctionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.observation = AgentObservation(
            round_number=0,
            environment=EnvironmentSnapshot(
                round_number=0,
                available_resources=80.0,
                maximum_capacity=100.0,
                regeneration_rate=5.0,
            ),
        )
        self.state = AgentState(agent_id=uuid4())

    def test_linear_utility_name_is_svo_implementation(self) -> None:
        self.assertIs(LinearUtilityFunction, SVOUtilityFunction)
        self.assertTrue(issubclass(SVOUtilityFunction, UtilityFunction))

    def test_profiles_use_expected_angles_and_independent_mutable_angles(self) -> None:
        profiles = (
            (Character.greedy(), 0.0),
            (Character.cooperative(), math.radians(64.0)),
            (Character.risk_averse(), math.radians(67.0)),
        )
        for character, expected_theta in profiles:
            self.assertAlmostEqual(character.theta, expected_theta)
            self.assertAlmostEqual(character.initial_theta, expected_theta)

        character = Character.cooperative()
        character.theta = 0.5
        self.assertAlmostEqual(character.initial_theta, math.radians(64.0))
        with self.assertRaises(AttributeError):
            character.initial_theta = 0.5  # type: ignore[misc]
        with self.assertRaises(ValueError):
            character.theta = math.pi

    def test_evaluates_wealth_and_projected_sustainability(self) -> None:
        character = Character(
            character_type=CharacterType.COOPERATIVE,
            theta=math.radians(64.0),
        )
        utility = SVOUtilityFunction()
        report = utility.evaluate_report(
            self.observation,
            AgentAction(extraction_amount=10.0),
            self.state,
            character,
        )

        self.assertAlmostEqual(report.chosen_w, 0.1**0.92)
        self.assertAlmostEqual(report.chosen_s, 0.735**0.85)
        self.assertAlmostEqual(
            report.wealth_weight,
            math.cos(math.radians(64.0)),
        )
        self.assertAlmostEqual(
            report.sustainability_weight,
            math.sin(math.radians(64.0)),
        )
        self.assertAlmostEqual(
            report.total_utility,
            math.cos(math.radians(64.0)) * (0.1**0.92)
            + math.sin(math.radians(64.0)) * (0.735**0.85),
        )

    def test_bounds_extraction_and_projected_stock(self) -> None:
        utility = SVOUtilityFunction()
        character = Character.greedy()
        exhausted_observation = AgentObservation(
            round_number=0,
            environment=EnvironmentSnapshot(
                round_number=0,
                available_resources=10.0,
                maximum_capacity=100.0,
                regeneration_rate=0.0,
            ),
        )
        report = utility.evaluate_report(
            exhausted_observation,
            AgentAction(extraction_amount=30.0),
            self.state,
            character,
        )

        self.assertAlmostEqual(report.chosen_w, 0.1**0.92)
        self.assertAlmostEqual(report.chosen_s, 0.0)
        self.assertAlmostEqual(report.total_utility, 0.1**0.92)

    def test_components_use_concave_power_scores(self) -> None:
        report = SVOUtilityFunction(
            wealth_exponent=0.92,
            sustainability_exponent=0.85,
        ).evaluate_report(
            self.observation,
            AgentAction(extraction_amount=10.0),
            self.state,
            Character.cooperative(),
        )
        self.assertAlmostEqual(report.chosen_w, 0.1**0.92)
        self.assertAlmostEqual(report.chosen_s, 0.735**0.85)
        self.assertGreater(report.chosen_w, 0.1)
        self.assertGreater(report.chosen_s, 0.75)

    def test_wealth_exponent_must_be_concave(self) -> None:
        with self.assertRaises(ValueError):
            SVOUtilityFunction(wealth_exponent=1.0)

    def test_sustainability_exponent_must_be_concave(self) -> None:
        with self.assertRaises(ValueError):
            SVOUtilityFunction(sustainability_exponent=1.0)

    def test_sustainability_caps_regeneration_at_capacity(self) -> None:
        observation = AgentObservation(
            round_number=0,
            environment=EnvironmentSnapshot(
                round_number=0,
                available_resources=99.0,
                maximum_capacity=100.0,
                regeneration_rate=10.0,
            ),
        )
        report = SVOUtilityFunction().evaluate_report(
            observation,
            AgentAction(extraction_amount=0.0),
            self.state,
            Character.cooperative(),
        )
        self.assertAlmostEqual(report.chosen_s, 1.0)

    def test_evaluate_candidates_preserves_action_order(self) -> None:
        reports = SVOUtilityFunction().evaluate_candidates(
            self.observation,
            [0.0, 5.0, 10.0],
            self.state,
            Character.cooperative(),
        )
        self.assertEqual(
            [report.action.extraction_amount for report in reports],
            [0.0, 5.0, 10.0],
        )


if __name__ == "__main__":
    unittest.main()
