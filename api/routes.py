from datetime import datetime, timezone
from math import isclose

from fastapi import APIRouter, HTTPException

from api.schemas import SimulationRequest
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
from simulation import Simulation

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}


@router.post("/simulations")
def run_simulation(request: SimulationRequest) -> dict[str, object]:
	agents = request.agents
	percentage_total = (
		agents.greedy_percentage
		+ agents.cooperative_percentage
		+ agents.risk_averse_percentage
	)
	if not isclose(percentage_total, 100.0, abs_tol=1e-6):
		raise HTTPException(
			status_code=422,
			detail="Agent percentages must sum to 100.",
		)

	environment = request.environment
	governance = request.governance
	config = SimulationConfig(
		environment=EnvironmentConfig(
			initial_resources=environment.initial_resources,
			maximum_capacity=max(environment.initial_resources, 1.0),
			regeneration_rate=environment.regeneration_rate,
			rounds=environment.rounds,
		),
		network=NetworkConfig(topology=NetworkTopology.COMPLETE),
		agents=AgentConfig(
			num_agents=agents.num_agents,
			greedy_percentage=agents.greedy_percentage,
			cooperative_percentage=agents.cooperative_percentage,
			risk_averse_percentage=agents.risk_averse_percentage,
		),
		governance=GovernanceConfig(
			quota_enabled=governance.quota_enabled,
			quota_limit=governance.quota_limit,
			tax_enabled=governance.tax_enabled,
			tax_rate=governance.tax_rate,
		),
		learning=LearningConfig(
			learning_algorithm=LearningAlgorithm.NO_LEARNING,
		),
	)

	simulation = Simulation(config)
	simulation.initialize()
	result = simulation.run()
	last_metrics = result.metrics_history[-1] if result.metrics_history else None

	return {
		"status": (
			"Resource Sustained"
			if result.final_resource_level > environment.initial_resources * 0.12
			else "Resource Collapsed"
		),
		"remainingResource": result.final_resource_level,
		"averageWealth": last_metrics.average_wealth if last_metrics else 0.0,
		"averageTrust": last_metrics.average_trust if last_metrics else 0.0,
		"chartData": [
			{
				"round": metrics.round_number,
				"resourceLevel": metrics.resource_level,
				"averageWealth": metrics.average_wealth,
			}
			for metrics in result.metrics_history
		],
		"completedAt": datetime.now(timezone.utc).isoformat(),
	}
