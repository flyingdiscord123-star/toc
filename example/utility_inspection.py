"""Inspect candidate utility scores for one agent."""

from __future__ import annotations

from uuid import uuid4

import networkx as nx

from agents.agent import Agent
from agents.character import Character
from agents.memory import AgentMemory
from agents.policies.utility_maximization import UtilityMaximizationPolicy
from agents.state import AgentState
from agents.utility import LinearUtilityFunction
from config.simulation_config import EnvironmentConfig
from environment.environment import Environment
from environment.resource_model import LinearResourceModel
from environment.resource_pool import ResourcePool
from network.graph_manager import GraphManager
from network.observer import ObservationBuilder
from learning.no_learning import NoLearning


def main() -> None:
    """Print utility reports and the policy's selected action."""
    environment_config = EnvironmentConfig(
        initial_resources=100.0,
        maximum_capacity=100.0,
        regeneration_rate=2.0,
        rounds=1,
    )
    resource_pool = ResourcePool(
        environment_config,
        LinearResourceModel(
            regeneration_rate=environment_config.regeneration_rate
        ),
    )
    environment = Environment(resource_pool)
    character = Character.greedy()
    utility_function = LinearUtilityFunction()
    agent = Agent(
        agent_id=0,
        state=AgentState(agent_id=uuid4()),
        character=character,
        memory=AgentMemory(),
        decision_policy=UtilityMaximizationPolicy(),
        utility_function=utility_function,
        learning=NoLearning(),
    )
    observation_builder = ObservationBuilder(
        GraphManager(nx.empty_graph(1)),
        [agent],
    )
    observation = observation_builder.build(
        agent_id=agent.id,
        environment=environment.snapshot(),
    )
    candidate_amounts = UtilityMaximizationPolicy.candidate_extraction_amounts
    reports = utility_function.evaluate_candidates(
        observation=observation,
        candidate_extraction_amounts=candidate_amounts,
        state=agent.state,
        character=agent.character,
    )

    print("Action  Wealth  Sustain  Trust  Compliance  Risk  Utility")
    print("-" * 62)
    for report in reports:
        print(
            f"{report.action.extraction_amount:>6.0f}  "
            f"{report.wealth:>6.2f}  "
            f"{report.sustainability:>7.2f}  "
            f"{report.trust:>5.2f}  "
            f"{report.compliance:>10.2f}  "
            f"{report.risk:>4.2f}  "
            f"{report.total_utility:>7.2f}"
        )

    chosen_action = agent.act(observation)
    report_action = max(
        reports,
        key=lambda report: report.total_utility,
    ).action
    assert chosen_action == report_action

    print("-" * 62)
    print(f"Chosen Action: {chosen_action.extraction_amount:g}")


if __name__ == "__main__":
    main()
