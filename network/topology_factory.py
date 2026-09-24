"""
topology_factory.py

Factory for constructing interaction network topologies.

The simulator never creates NetworkX graphs directly.
Instead, it requests a topology from this factory.
"""

from __future__ import annotations

import networkx as nx

from config.simulation_config import NetworkConfig

from .graph_manager import GraphManager


class TopologyFactory:
    """
    Factory responsible for constructing interaction networks.
    """

    @classmethod
    def create(
        cls,
        config: NetworkConfig,
        num_agents: int,
    ) -> GraphManager:
        """
        Construct the configured network topology.

        Parameters
        ----------
        config:
            Network configuration.

        num_agents:
            Number of agents in the simulation.
        """

        topology = config.topology.value.lower()

        if topology == "complete":

            graph = nx.complete_graph(num_agents)

        elif topology == "ring":

            graph = nx.cycle_graph(num_agents)

        elif topology == "random":

            graph = nx.erdos_renyi_graph(
                n=num_agents,
                p=config.rewiring_probability,
                seed=config.random_seed,
            )

        elif topology == "small_world":

            graph = nx.watts_strogatz_graph(
                n=num_agents,
                k=config.average_degree,
                p=config.rewiring_probability,
                seed=config.random_seed,
            )

        elif topology == "scale_free":

            graph = nx.barabasi_albert_graph(
                n=num_agents,
                m=max(1, config.average_degree // 2),
                seed=config.random_seed,
            )

        else:

            raise ValueError(
                f"Unknown topology '{config.topology}'."
            )

        return GraphManager(graph)