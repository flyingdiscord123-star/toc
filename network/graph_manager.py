"""
graph_manager.py

Provides a thin wrapper around the underlying graph representation.

The GraphManager owns the simulation network and exposes a minimal API
for querying neighborhood relationships. The rest of the simulator
should never interact with NetworkX directly.

Responsibilities
----------------
- Store the interaction graph.
- Expose neighborhood queries.
- Hide NetworkX implementation details.
"""

from __future__ import annotations

from collections.abc import Sequence

import networkx as nx


class GraphManager:
    """
    Manages the interaction network between agents.
    """

    def __init__(
        self,
        graph: nx.Graph,
    ) -> None:
        self._graph = graph

    @property
    def graph(self) -> nx.Graph:
        """
        Return the underlying NetworkX graph.

        This property exists primarily for visualization and debugging.
        Most code should use the GraphManager interface instead.
        """
        return self._graph

    def neighbors(
        self,
        agent_id: int,
    ) -> tuple[int, ...]:
        """
        Return the neighboring agent IDs.
        """

        return tuple(self._graph.neighbors(agent_id))

    def degree(
        self,
        agent_id: int,
    ) -> int:
        """
        Return the degree of an agent.
        """

        return self._graph.degree(agent_id)

    def number_of_agents(self) -> int:
        """
        Return the number of nodes in the network.
        """

        return self._graph.number_of_nodes()

    def has_edge(
        self,
        agent_a: int,
        agent_b: int,
    ) -> bool:
        """
        Check whether two agents are connected.
        """

        return self._graph.has_edge(agent_a, agent_b)

    def nodes(self) -> Sequence[int]:
        """
        Return all agent IDs.
        """

        return tuple(self._graph.nodes())