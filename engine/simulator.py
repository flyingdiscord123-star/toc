"""
simulator.py

Defines the main simulation engine.

The Simulator orchestrates interactions between the environment,
agents, scheduler, and (later) governance, learning, and metrics.

The Simulator intentionally contains no decision-making logic,
resource regeneration logic, or governance rules.
"""

from __future__ import annotations
from agents import observation
from trust.trust_engine import TrustEngine
from governance.engine import RuleEngine
from governance.registry import RuleRegistry
from governance.rules.quota_rule import QuotaRule
from agents.agent import Agent
from agents.experience import AgentExperience
from agents.observation import AgentObservation
from config.simulation_config import SimulationConfig
from environment.environment import Environment
from .result import SimulationResult
from .scheduler import Scheduler
from network.observer import ObservationBuilder
from governance.context import RuleContext
from governance.engine import RuleEngine
from metrics.collector import MetricsCollector
from metrics.round_metrics import RoundMetrics
class Simulator:
    """
    Coordinates the execution of a simulation.

    The Simulator is the only component that knows about all major
    subsystems.
    """

    def __init__(
        self,
        config: SimulationConfig,
        environment: Environment,
        agents: list[Agent],
        scheduler: Scheduler,
        observation_builder: ObservationBuilder,
        rule_engine: RuleEngine,
        trust_engine: TrustEngine,
        metrics_collector: MetricsCollector,
    ) -> None:
        self._config = config
        self._environment = environment
        self._agents = agents
        self._scheduler = scheduler
        self._observation_builder = observation_builder
        self._rule_engine = rule_engine
        self._trust_engine = trust_engine
        self._metrics_collector = metrics_collector

    @property
    def config(self) -> SimulationConfig:
        """
        Configuration used by this simulation.
        """
        return self._config

    def run(self) -> SimulationResult:
        """
        Execute the simulation.

        Returns
        -------
        SimulationResult
            Summary of the completed simulation.
        """

        rounds = self._config.environment.rounds

        for _ in range(rounds):

            violations = 0
            successful_extractions = 0

            environment_snapshot = self._environment.snapshot()

            ordered_agents = self._scheduler.order(self._agents)

            for agent in ordered_agents:

                observation = self._observation_builder.build(
                agent_id=agent.id,
                environment=environment_snapshot,
        )

                agent.observe(observation)
                

                
                action = agent.act(observation)
                context = RuleContext(
                    agent=agent,
                    action=action,
                    environment=environment_snapshot,
                )
                rule_result = self._rule_engine.evaluate(context)
                
                if not rule_result.allowed:
                    violations += 1
                    extracted = 0.0

                else:
                    extracted = self._environment.resource_pool.extract(
                    action.extraction_amount,
                )
                    if extracted > 0.0:
                        successful_extractions += 1


                

                agent.receive_resources(extracted)
                next_snapshot = self._environment.snapshot()

                next_observation = self._observation_builder.build(
                agent_id=agent.id,
                environment=next_snapshot,
                )

                experience = AgentExperience(
                    observation=observation,
                    action=action,
                    next_observation=next_observation,
                    outcome={
                        "resources_extracted": extracted,
                    },
                )

                agent.remember(experience)
                self._trust_engine.update(
                source=agent.id,
                target=agent.id,
                successful_interaction=rule_result.allowed,
            )

                agent.learn(experience)

            self._environment.step()

            average_wealth = sum(
                agent.state.wealth for agent in self._agents
            ) / len(self._agents)
            total_wealth = sum(
                agent.state.wealth for agent in self._agents
            )

            self._metrics_collector.record(
                RoundMetrics(
                round_number=self._environment.round_number,
                resource_level=(
                    self._environment.resource_pool.available_resources
                ),
                average_wealth=average_wealth,
                total_wealth=total_wealth,
                average_trust=self._trust_engine.average_trust(),
                violations=violations,
                successful_extractions=successful_extractions,
                )
            )

        return SimulationResult(
        rounds_completed=self._environment.round_number,
        final_resource_level=self._environment.resource_pool.available_resources,
        agent_wealth={
            agent.id: agent.state.wealth
            for agent in self._agents
        },
        metrics_history=list(self._metrics_collector.history),
)