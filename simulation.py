"""
simulation.py

Top-level Simulation object.

The Simulation class owns the complete configuration for one
simulation run.

The Simulation owns construction of the components required by one
simulation run and delegates execution to the Simulator.
"""

from __future__ import annotations

from uuid import uuid4

import networkx as nx

from agents.agent import Agent
from agents.character import Character
from agents.memory import AgentMemory
from agents.policies.utility_maximization import UtilityMaximizationPolicy
from agents.state import AgentState
from agents.utility import LinearUtilityFunction
from config.simulation_config import (
    CharacterType,
    NetworkTopology,
    SimulationConfig,
)
from engine.result import SimulationResult
from engine.scheduler import SequentialScheduler
from engine.simulator import Simulator
from environment.environment import Environment
from environment.resource_model import LinearResourceModel
from environment.resource_pool import ResourcePool
from governance.engine import RuleEngine
from governance.registry import RuleRegistry
from governance.rules.quota_rule import QuotaRule
from learning.factory import LearningFactory
from metrics.collector import MetricsCollector
from network.graph_manager import GraphManager
from network.observer import ObservationBuilder
from trust.trust_engine import TrustEngine
from trust.trust_matrix import TrustMatrix
from trust.trust_update import LinearTrustUpdate


class Simulation:
    """
    Represents a single simulation instance.

    Each Simulation owns exactly one immutable configuration.

    Future responsibilities include:

    - constructing the environment
    - constructing the agent population
    - building the interaction network
    - executing the simulation loop
    - collecting metrics
    """

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config

        self._resource_model: LinearResourceModel | None = None
        self._resource_pool: ResourcePool | None = None
        self._environment: Environment | None = None
        self._graph_manager: GraphManager | None = None
        self._observation_builder: ObservationBuilder | None = None
        self._scheduler: SequentialScheduler | None = None
        self._rule_registry: RuleRegistry | None = None
        self._rule_engine: RuleEngine | None = None
        self._trust_matrix: TrustMatrix | None = None
        self._trust_updater: LinearTrustUpdate | None = None
        self._trust_engine: TrustEngine | None = None
        self._metrics_collector: MetricsCollector | None = None
        self._agents: list[Agent] | None = None
        self._simulator: Simulator | None = None

    def initialize(self) -> None:
        """
        Build all simulation components.
        """
        if self._simulator is not None:
            return

        self._resource_model = LinearResourceModel(
            regeneration_rate=self.config.environment.regeneration_rate,
        )
        self._resource_pool = ResourcePool(
            self.config.environment,
            self._resource_model,
        )
        self._environment = Environment(self._resource_pool)

        self._graph_manager = self._create_graph()
        self._agents = self._create_agents()
        self._observation_builder = ObservationBuilder(
            self._graph_manager,
            self._agents,
        )
        self._scheduler = SequentialScheduler()

        self._rule_registry = RuleRegistry()
        self._rule_registry.register(
            QuotaRule(maximum_extraction=20.0)
        )
        self._rule_engine = RuleEngine(self._rule_registry)

        self._trust_matrix = TrustMatrix()
        self._trust_updater = LinearTrustUpdate()
        self._trust_engine = TrustEngine(
            matrix=self._trust_matrix,
            updater=self._trust_updater,
        )
        self._metrics_collector = MetricsCollector()

        self._simulator = Simulator(
            config=self.config,
            environment=self._environment,
            agents=self._agents,
            scheduler=self._scheduler,
            observation_builder=self._observation_builder,
            rule_engine=self._rule_engine,
            trust_engine=self._trust_engine,
            metrics_collector=self._metrics_collector,
        )

    def run(self) -> SimulationResult:
        """
        Execute the simulation.
        """
        if self._simulator is None:
            raise RuntimeError(
                "Simulation must be initialized before it can be run."
            )

        return self._simulator.run()

    def _create_graph(self) -> GraphManager:
        """Create the configured interaction graph."""
        if self.config.network.topology is not NetworkTopology.COMPLETE:
            raise NotImplementedError(
                "Only the COMPLETE network topology is currently supported."
            )

        return GraphManager(
            nx.complete_graph(self.config.agents.num_agents)
        )

    def _create_agents(self) -> list[Agent]:
        """Create the configured population of simulation agents."""
        return [
            self._create_agent(agent_id)
            for agent_id in range(self.config.agents.num_agents)
        ]

    def _create_agent(self, agent_id: int) -> Agent:
        """Create one agent using the configured population distribution."""
        character_type = self._character_type_for(agent_id)
        character = self._character_for(character_type)

        return Agent(
            agent_id=agent_id,
            state=AgentState(agent_id=uuid4(), wealth=0.0),
            character=character,
            memory=AgentMemory(),
            decision_policy=UtilityMaximizationPolicy(),
            utility_function=LinearUtilityFunction(),
            learning=LearningFactory.create(
                self.config.learning.learning_algorithm.value
            ),
        )

    def _character_type_for(self, agent_id: int) -> CharacterType:
        """Choose an agent character deterministically from configured shares."""
        config = self.config.agents
        population = (
            (CharacterType.GREEDY, config.percentage_greedy),
            (CharacterType.COOPERATIVE, config.percentage_cooperative),
            (CharacterType.RISK_AVERSE, config.percentage_risk_averse),
            (CharacterType.OPPORTUNIST, config.percentage_opportunist),
        )
        position = (agent_id + 0.5) * 100 / config.num_agents
        cumulative = 0.0

        for character_type, percentage in population:
            cumulative += percentage
            if position <= cumulative:
                return character_type

        return CharacterType.OPPORTUNIST

    @staticmethod
    def _character_for(character_type: CharacterType) -> Character:
        """Create the utility profile associated with a character type."""
        mapping = {
            CharacterType.GREEDY: Character.greedy,
            CharacterType.COOPERATIVE: Character.cooperative,
            CharacterType.RISK_AVERSE: Character.risk_averse,
            CharacterType.OPPORTUNIST: Character.opportunistic,
        }
        return mapping[character_type]()