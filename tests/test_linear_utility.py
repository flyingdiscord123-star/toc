"""Focused tests for the modular linear utility subsystem."""

from __future__ import annotations

import unittest
from uuid import uuid4

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility import (
    ComplianceComponent,
    LinearUtilityFunction,
    RiskComponent,
    SustainabilityComponent,
    TrustComponent,
    UtilityContext,
    UtilityFunction,
    WealthComponent,
)
from agents.utility.component import UtilityComponent
from agents.utility_weights import UtilityWeights
from config.simulation_config import CharacterType
from environment.environment import EnvironmentSnapshot


class FixedComponent(UtilityComponent):
    """Test component returning a fixed score and tracking evaluations."""

    def __init__(self, score: float) -> None:
        self.score = score
        self.calls = 0

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        self.calls += 1
        return self.score


class LinearUtilityFunctionTests(unittest.TestCase):
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
        self.action = AgentAction(extraction_amount=4.0)
        self.state = AgentState(agent_id=uuid4())
        self.character = Character(
            character_type=CharacterType.GREEDY,
            utility_weights=UtilityWeights(
                wealth=3.0,
                sustainability=4.0,
                trust=5.0,
                compliance=6.0,
                risk=7.0,
            ),
        )

    def test_is_a_utility_function(self) -> None:
        self.assertTrue(
            issubclass(LinearUtilityFunction, UtilityFunction)
        )

    def test_utility_context_is_immutable(self) -> None:
        context = UtilityContext(
            observation=self.observation,
            action=self.action,
            state=self.state,
            character=self.character,
        )

        with self.assertRaises(AttributeError):
            context.action = AgentAction(extraction_amount=8.0)  # type: ignore[misc]

    def test_evaluates_each_component_once(self) -> None:
        components = [FixedComponent(score) for score in range(1, 6)]
        utility = LinearUtilityFunction(*components)

        utility.evaluate(
            observation=self.observation,
            action=self.action,
            state=self.state,
            character=self.character,
        )

        for component in components:
            self.assertEqual(component.calls, 1)

    def test_context_is_passed_to_components(self) -> None:
        component = FixedComponent(1.0)
        utility = LinearUtilityFunction(
            wealth=component,
            sustainability=component,
            trust=component,
            compliance=component,
            risk=component,
        )

        utility.evaluate(
            observation=self.observation,
            action=self.action,
            state=self.state,
            character=self.character,
        )

        self.assertEqual(component.calls, 5)

    def test_baseline_component_scores_are_normalized(self) -> None:
        context = UtilityContext(
            observation=self.observation,
            action=AgentAction(extraction_amount=10.0),
            state=self.state,
            character=self.character,
        )
        components = (
            WealthComponent(),
            SustainabilityComponent(),
            TrustComponent(),
            ComplianceComponent(),
            RiskComponent(),
        )

        for component in components:
            score = component.evaluate(context)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_applies_character_weights(self) -> None:
        components = [
            FixedComponent(2.0),
            FixedComponent(1.0),
            FixedComponent(0.5),
            FixedComponent(2.0),
            FixedComponent(1.0),
        ]
        utility = LinearUtilityFunction(*components)

        result = utility.evaluate(
            observation=self.observation,
            action=self.action,
            state=self.state,
            character=self.character,
        )

        self.assertEqual(result, 17.5)

    def test_subtracts_risk(self) -> None:
        character = Character(
            character_type=CharacterType.GREEDY,
            utility_weights=UtilityWeights(
                wealth=1.0,
                sustainability=0.0,
                trust=0.0,
                compliance=0.0,
                risk=1.0,
            ),
        )
        utility = LinearUtilityFunction(
            FixedComponent(10.0),
            FixedComponent(0.0),
            FixedComponent(0.0),
            FixedComponent(0.0),
            FixedComponent(2.0),
        )

        result = utility.evaluate(
            observation=self.observation,
            action=self.action,
            state=self.state,
            character=character,
        )

        self.assertEqual(result, 8.0)

    def test_custom_components_can_be_injected(self) -> None:
        wealth = FixedComponent(6.0)
        utility = LinearUtilityFunction(
            wealth=wealth,
            sustainability=FixedComponent(0.0),
            trust=FixedComponent(0.0),
            compliance=FixedComponent(0.0),
            risk=FixedComponent(0.0),
        )
        character = Character(
            character_type=CharacterType.GREEDY,
            utility_weights=UtilityWeights(
                wealth=2.0,
                sustainability=0.0,
                trust=0.0,
                compliance=0.0,
                risk=0.0,
            ),
        )

        result = utility.evaluate(
            observation=self.observation,
            action=self.action,
            state=self.state,
            character=character,
        )

        self.assertEqual(result, 12.0)
        self.assertEqual(wealth.calls, 1)

    def test_evaluate_candidates_returns_ordered_reports(self) -> None:
        utility = LinearUtilityFunction()

        reports = utility.evaluate_candidates(
            observation=self.observation,
            candidate_extraction_amounts=[0, 2, 4],
            state=self.state,
            character=self.character,
        )

        self.assertEqual(
            [report.action.extraction_amount for report in reports],
            [0, 2, 4],
        )
        for report in reports:
            self.assertEqual(
                report.total_utility,
                (
                    self.character.utility_weights.wealth * report.wealth
                    + self.character.utility_weights.sustainability
                    * report.sustainability
                    + self.character.utility_weights.trust * report.trust
                    + self.character.utility_weights.compliance
                    * report.compliance
                    - self.character.utility_weights.risk * report.risk
                ),
            )


if __name__ == "__main__":
    unittest.main()
