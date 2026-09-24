"""
smoke_test.py

Architecture smoke test.

Verifies that the major components of the Commons Simulator
can be instantiated and interact correctly.
"""

from uuid import uuid4

import networkx as nx

from agents.agent import Agent
from agents.character import Character
from agents.memory import AgentMemory
from agents.policies.utility_maximization import UtilityMaximizationPolicy
from agents.state import AgentState
from agents.utility import LinearUtilityFunction

from config.simulation_config import (
    AgentConfig,
    CharacterType,
    EnvironmentConfig,
    GovernanceConfig,
    LearningAlgorithm,
    LearningConfig,
    NetworkConfig,
    NetworkTopology,
    SimulationConfig,
)

from environment.environment import Environment
from environment.resource_model import LinearResourceModel
from environment.resource_pool import ResourcePool

from learning.no_learning import NoLearning

from network.graph_manager import GraphManager
from network.observer import ObservationBuilder
from simulation import Simulation


def make_agent(agent_id: int) -> Agent:
    character = Character.greedy()

    return Agent(
        agent_id=agent_id,
        state=AgentState(agent_id=uuid4(), wealth=0.0),
        character=character,
        memory=AgentMemory(),
        decision_policy=UtilityMaximizationPolicy(),
        utility_function=LinearUtilityFunction(),
        learning=NoLearning(),
    )


def main() -> None:

    print("=====================================")
    print("Commons Simulator Smoke Test")
    print("=====================================\n")

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
    print("✓ SimulationConfig")

    resource_model = LinearResourceModel(
        regeneration_rate=config.environment.regeneration_rate,
    )
    print("✓ ResourceModel")

    resource_pool = ResourcePool(
        config.environment,
        resource_model,
    )
    print("✓ ResourcePool")

    environment = Environment(resource_pool)
    print("✓ Environment")

    graph = nx.complete_graph(config.agents.num_agents)
    graph_manager = GraphManager(graph)
    print("✓ GraphManager")

    agents = [
        make_agent(0),
        make_agent(1),
    ]
    print("✓ Agents")

    observation_builder = ObservationBuilder(
        graph_manager,
        agents,
    )
    print("✓ ObservationBuilder")

    observation = observation_builder.build(
        agent_id=0,
        environment=environment.snapshot(),
    )
    print("✓ AgentObservation")

    action = agents[0].act(observation)
    print("✓ DecisionPolicy")

    agents[0].receive_resources(5.0)
    print("✓ Agent state update")

    print()
    print("Observation Summary")
    print("-------------------")
    print(f"Round: {observation.round_number}")
    print(f"Neighbors: {len(observation.neighbors)}")
    print(f"Action: extract {action.extraction_amount}")
    print(f"Wealth: {agents[0].state.wealth}")

    simulation = Simulation(config)
    simulation.initialize()
    result = simulation.run()
    assert len(result.metrics_history) == config.environment.rounds
    assert (
        result.metrics_history[-1].resource_level
        == result.final_resource_level
    )
    print("✓ Metrics history")

    print("\n=====================================")
    print("Smoke Test Passed")
    print("=====================================")


if __name__ == "__main__":
    main()