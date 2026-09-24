from simulation import Simulation

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
        greedy_percentage=100,
        cooperative_percentage=0,
        risk_averse_percentage=0,
    ),
    governance=GovernanceConfig(),
    learning=LearningConfig(
        learning_algorithm=LearningAlgorithm.NO_LEARNING,
    ),
)

simulation = Simulation(config)

simulation.initialize()

result = simulation.run()

print(result)



print("PASS")