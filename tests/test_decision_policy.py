from __future__ import annotations

import unittest
from uuid import uuid4

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.policies.utility_maximization import UtilityMaximizationPolicy
from agents.state import AgentState
from agents.utility import LinearUtilityFunction, UtilityFunction
from config.simulation_config import (
    AgentConfig,
    DecisionConfig,
    EnvironmentConfig,
    GovernanceConfig,
    LearningAlgorithm,
    LearningConfig,
    NetworkConfig,
    NetworkTopology,
    SimulationConfig,
)
from environment.environment import EnvironmentSnapshot
from simulation import Simulation


class HarvestAmountUtility(UtilityFunction):
    def __init__(self) -> None:
        self.calls = 0

    def evaluate(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> float:
        self.calls += 1
        return action.extraction_amount


class UtilityMaximizationPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.observation = AgentObservation(
            round_number=0,
            environment=EnvironmentSnapshot(
                round_number=0,
                available_resources=100.0,
                maximum_capacity=100.0,
                regeneration_rate=0.0,
            ),
            quota_limit=4.0,
        )
        self.state = AgentState(agent_id=uuid4())
        self.character = Character.greedy()
        self.utility = HarvestAmountUtility()

    def test_decision_configuration_defaults_and_validates_probability(self) -> None:
        self.assertEqual(DecisionConfig().exploration_probability, 0.25)
        with self.assertRaises(ValueError):
            DecisionConfig(exploration_probability=-0.1)
        with self.assertRaises(ValueError):
            DecisionConfig(exploration_probability=1.1)

    def test_zero_exploration_always_selects_the_same_best_action(self) -> None:
        policy = UtilityMaximizationPolicy(
            DecisionConfig(exploration_probability=0.0),
            quota_limit=4.0,
        )

        chosen = [
            policy.decide(
                self.observation,
                self.state,
                self.character,
                self.utility,
            ).extraction_amount
            for _ in range(10)
        ]

        self.assertEqual(chosen, [4.0] * 10)

    def test_exploration_probability_produces_stochastic_choices(self) -> None:
        policy = UtilityMaximizationPolicy(
            DecisionConfig(exploration_probability=0.25),
            quota_limit=4.0,
            random_seed=42,
        )

        chosen = {
            policy.decide(
                self.observation,
                self.state,
                self.character,
                self.utility,
            ).extraction_amount
            for _ in range(100)
        }

        self.assertGreater(len(chosen), 1)
        self.assertIn(4.0, chosen)

    def test_candidate_utilities_are_ranked_highest_first(self) -> None:
        policy = UtilityMaximizationPolicy(quota_limit=4.0)
        ranked = policy.rank_candidates(
            observation=self.observation,
            state=self.state,
            character=self.character,
            utility_function=self.utility,
        )

        utilities = [utility for _, utility in ranked]
        self.assertEqual(utilities, sorted(utilities, reverse=True))
        self.assertEqual(ranked[0][0].extraction_amount, 4.0)
        self.assertEqual(self.utility.calls, 5)

    def test_top_k_is_ceil_of_half_the_candidate_space(self) -> None:
        self.assertEqual(UtilityMaximizationPolicy.top_k_size(5), 3)
        self.assertEqual(UtilityMaximizationPolicy.top_k_size(21), 11)

    def test_exploration_never_selects_the_top_ranked_action(self) -> None:
        policy = UtilityMaximizationPolicy(
            DecisionConfig(exploration_probability=1.0),
            quota_limit=4.0,
            random_seed=17,
        )

        chosen = [
            policy.decide(
                self.observation,
                self.state,
                self.character,
                self.utility,
            ).extraction_amount
            for _ in range(25)
        ]

        self.assertNotIn(4.0, chosen)
        self.assertTrue(all(1.0 <= amount <= 3.0 for amount in chosen))

    def test_candidates_and_selected_actions_respect_the_quota(self) -> None:
        policy = UtilityMaximizationPolicy(
            DecisionConfig(exploration_probability=1.0),
            quota_limit=3.5,
            random_seed=1,
        )
        observation = AgentObservation(
            round_number=0,
            environment=self.observation.environment,
            quota_limit=3.5,
        )

        self.assertEqual(
            policy.candidate_extraction_amounts(),
            [0.0, 1.0, 2.0, 3.0, 3.5],
        )
        chosen = policy.decide(
            observation,
            self.state,
            self.character,
            self.utility,
        )
        self.assertLessEqual(chosen.extraction_amount, 3.5)

    def test_seeded_simulations_record_harvest_metrics_reproducibly(self) -> None:
        config = SimulationConfig(
            environment=EnvironmentConfig(
                initial_resources=100.0,
                maximum_capacity=100.0,
                regeneration_rate=2.0,
                rounds=5,
            ),
            network=NetworkConfig(
                topology=NetworkTopology.COMPLETE,
                random_seed=31,
            ),
            agents=AgentConfig(
                num_agents=3,
                greedy_percentage=33.3333333333,
                cooperative_percentage=33.3333333333,
                risk_averse_percentage=33.3333333334,
            ),
            governance=GovernanceConfig(quota_limit=5.0),
            learning=LearningConfig(
                learning_algorithm=LearningAlgorithm.NO_LEARNING,
            ),
            decision=DecisionConfig(exploration_probability=0.25),
        )

        first = Simulation(config)
        first.initialize()
        first_result = first.run()

        second = Simulation(config)
        second.initialize()
        second_result = second.run()

        self.assertEqual(len(first_result.metrics_history), 5)
        self.assertEqual(
            first_result.metrics_history,
            second_result.metrics_history,
        )
        for metrics in first_result.metrics_history:
            self.assertLessEqual(metrics.average_harvest_greedy, 5.0)
            self.assertLessEqual(metrics.average_harvest_cooperative, 5.0)
            self.assertLessEqual(metrics.average_harvest_risk_averse, 5.0)

    def test_simulation_uses_one_shared_utility_function(self) -> None:
        config = SimulationConfig(
            environment=EnvironmentConfig(100.0, 100.0, 2.0, 1),
            network=NetworkConfig(NetworkTopology.COMPLETE),
            agents=AgentConfig(3, 33.3333333333, 33.3333333333, 33.3333333334),
            governance=GovernanceConfig(quota_limit=5.0),
            learning=LearningConfig(
                learning_algorithm=LearningAlgorithm.NO_LEARNING,
            ),
        )
        simulation = Simulation(config)
        simulation.initialize()

        agents = simulation._agents
        self.assertIsNotNone(agents)
        self.assertTrue(
            all(
                agent.utility_function is agents[0].utility_function
                for agent in agents
            )
        )

    def test_zero_exploration_simulations_are_deterministic_without_a_seed(self) -> None:
        config = SimulationConfig(
            environment=EnvironmentConfig(100.0, 100.0, 2.0, 3),
            network=NetworkConfig(NetworkTopology.COMPLETE),
            agents=AgentConfig(3, 33.3333333333, 33.3333333333, 33.3333333334),
            governance=GovernanceConfig(quota_limit=5.0),
            learning=LearningConfig(
                learning_algorithm=LearningAlgorithm.NO_LEARNING,
            ),
            decision=DecisionConfig(exploration_probability=0.0),
        )

        first = Simulation(config)
        first.initialize()
        second = Simulation(config)
        second.initialize()

        self.assertEqual(
            first.run().metrics_history,
            second.run().metrics_history,
        )


if __name__ == "__main__":
    unittest.main()
