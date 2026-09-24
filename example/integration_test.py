"""
integration_test.py

Runs a minimal end-to-end simulation.

This verifies that all core components of the Commons Simulator
work together correctly.
"""

from config.simulation_config import (
    CharacterType,
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


def main():

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

    assert len(result.metrics_history) == config.environment.rounds
    assert (
        result.metrics_history[-1].resource_level
        == result.final_resource_level
    )

    print("\n==============================")
    print("Simulation Finished")
    print("==============================\n")

    print(f"Rounds completed : {result.rounds_completed}")
    print(f"Resources left   : {result.final_resource_level:.2f}")

    print("\nAgent Wealth")

    for agent_id, wealth in result.agent_wealth.items():
        print(f"Agent {agent_id}: {wealth:.2f}")

    print("\nPASS")


if __name__ == "__main__":
    main()