"""Tests for API simulation configuration."""

from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from api.routes import run_simulation
from api.schemas import SimulationRequest
from config.simulation_config import LearningAlgorithm


class SimulationRouteTests(unittest.TestCase):
    def test_api_enables_svo_gradient_learning_with_default_parameters(self) -> None:
        request = SimulationRequest(
            agents={
                "numAgents": 1,
                "greedyPercentage": 0.0,
                "cooperativePercentage": 100.0,
                "riskAversePercentage": 0.0,
            },
            environment={
                "initialResources": 100.0,
                "regenerationRate": 2.0,
                "rounds": 1,
            },
            governance={
                "quotaEnabled": True,
                "quotaLimit": 20.0,
                "taxEnabled": False,
                "taxRate": 0.0,
            },
            explorationProbability=0.0,
        )
        fake_result = SimpleNamespace(
            final_resource_level=100.0,
            metrics_history=[],
        )

        with patch("api.routes.Simulation") as simulation_factory:
            simulation = simulation_factory.return_value
            simulation.run.return_value = fake_result

            run_simulation(request)

        simulation_config = simulation_factory.call_args.args[0]
        self.assertEqual(
            simulation_config.learning.learning_algorithm,
            LearningAlgorithm.SVO_GRADIENT,
        )
        self.assertEqual(simulation_config.learning.learning_rate, 0.01)
        self.assertEqual(simulation_config.learning.anchor_lambda, 0.20)
        simulation.initialize.assert_called_once()
        simulation.run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
