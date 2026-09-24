from experiments.experiment import Experiment
from experiments.experiment_result import ExperimentResult
from experiments.seeds import SeedGenerator
from experiments.statistics import Statistics

from config.simulation_config import (
    SimulationConfig,
    EnvironmentConfig,
    NetworkConfig,
    AgentConfig,
    GovernanceConfig,
    LearningConfig,
    LearningAlgorithm,
    NetworkTopology,
)

config = SimulationConfig(
    environment=EnvironmentConfig(
        initial_resources=100,
        maximum_capacity=100,
        regeneration_rate=2,
        rounds=5,
    ),
    network=NetworkConfig(
        topology=NetworkTopology.COMPLETE,
    ),
    agents=AgentConfig(
        num_agents=2,
        percentage_greedy=100,
        percentage_cooperative=0,
        percentage_risk_averse=0,
        percentage_opportunist=0,
    ),
    governance=GovernanceConfig(),
    learning=LearningConfig(
        learning_algorithm=LearningAlgorithm.NO_LEARNING,
    ),
)

experiment = Experiment(config)
print("✓ Experiment created")

results = ExperimentResult(results=[])
print("✓ ExperimentResult created")

seed = SeedGenerator()
print(seed.next_seed())
print(seed.next_seed())
print(seed.next_seed())

print("PASS")