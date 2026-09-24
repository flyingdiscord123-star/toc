"""
observer.py

Constructs AgentObservation objects.

The ObservationBuilder gathers information from the environment
and interaction network to create the observations supplied to
individual agents.

The simulator delegates observation construction to this class,
keeping orchestration separate from data assembly.
"""

from __future__ import annotations
from agents.agent import Agent
from agents.observation import (
    AgentObservation,
    NeighborObservation,
)
from environment.environment import EnvironmentSnapshot

from .graph_manager import GraphManager


class ObservationBuilder:
    """
    Builds observations for agents.
    """

    def __init__(
        self,
        graph_manager: GraphManager,
        agents: list[Agent],
    ) -> None:
        self._graph_manager = graph_manager

        self._agents = {
            agent.id: agent
            for agent in agents
        }

    def build(
        self,
        agent_id: int,
        environment: EnvironmentSnapshot,
    ) -> AgentObservation:
        """
        Construct the observation for a single agent.
        """

        neighbors = []

        for neighbor_id in self._graph_manager.neighbors(agent_id):

            neighbor = self._agents[neighbor_id]

            neighbors.append(
        NeighborObservation(
            agent_id=neighbor.id,
            wealth=neighbor.state.wealth,
            alive=neighbor.state.alive,
                )
            )

        neighbors = tuple(neighbors)
        return AgentObservation(
            round_number=environment.round_number,
            environment=environment,
            neighbors=neighbors,
            governance_signals={},
            metadata={},
        )