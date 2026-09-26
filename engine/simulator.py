"""
simulator.py

Defines the main simulation engine.

The Simulator orchestrates interactions between the environment,
agents, scheduler, and (later) governance, learning, and metrics.

The Simulator intentionally contains no decision-making logic,
resource regeneration logic, or governance rules.
"""

from __future__ import annotations
from economics.economic_outcome import EconomicOutcome
from agents import observation
from trust.trust_engine import TrustEngine
from governance.action_outcome import ActionOutcome
from governance.mechanisms.registry import GovernanceMechanismRegistry
from agents.agent import Agent
from agents.experience import AgentExperience
from agents.observation import AgentObservation
from config.simulation_config import SimulationConfig
from environment.environment import Environment
from .result import SimulationResult
from .scheduler import Scheduler
from network.observer import ObservationBuilder
from metrics.collector import MetricsCollector
from metrics.round_metrics import RoundMetrics
from learning.experience import LearningExperience
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
        mechanism_registry: GovernanceMechanismRegistry,
        trust_engine: TrustEngine,
        metrics_collector: MetricsCollector,
    ) -> None:
        self._config = config
        self._environment = environment
        self._agents = agents
        self._scheduler = scheduler
        self._observation_builder = observation_builder
        self._mechanism_registry = mechanism_registry
        self._trust_engine = trust_engine
        self._metrics_collector = metrics_collector

    @property
    def config(self) -> SimulationConfig:
        """
        Configuration used by this simulation.
        """
        return self._config

    def run(self) -> SimulationResult:
        """Execute the simulation and return its completed result."""
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
                action_outcome = ActionOutcome(
                    requested_extraction=action.extraction_amount,
                    approved_extraction=action.extraction_amount,
                    net_resources_received=action.extraction_amount,
                    tax_paid=0.0,
                    subsidy_received=0.0,
                    compliant=True,
                    violation_reason=None,
                )
                action_outcome = self._mechanism_registry.apply_all(
                    action=action,
                    observation=observation,
                    environment=environment_snapshot,
                    outcome=action_outcome,
                )
                extracted = self._environment.resource_pool.extract(
                    action_outcome.approved_extraction
                )
                action_outcome = ActionOutcome(
                    requested_extraction=action_outcome.requested_extraction,
                    approved_extraction=action_outcome.approved_extraction,
                    net_resources_received=extracted,
                    tax_paid=action_outcome.tax_paid,
                    subsidy_received=action_outcome.subsidy_received,
                    compliant=action_outcome.compliant,
                    violation_reason=action_outcome.violation_reason,
                )

                if action_outcome.net_resources_received > 0.0:
                    successful_extractions += 1
                if not action_outcome.compliant:
                    violations += 1

                economic_outcome = EconomicOutcome.from_action_outcome(
                    action_outcome
                )
                agent.state.wealth += economic_outcome.net_income
                utility_report = agent.utility_function.evaluate_report(
                    observation=observation,
                    action=action,
                    state=agent.state,
                    character=agent.character,
                )
                learning_experience = LearningExperience(
                    observation=observation,
                    chosen_action=action,
                    economic_outcome=economic_outcome,
                    utility_component_scores=(
                        ("wealth", utility_report.wealth),
                        (
                            "sustainability",
                            utility_report.sustainability,
                        ),
                        ("trust", utility_report.trust),
                        ("compliance", utility_report.compliance),
                        ("risk", utility_report.risk),
                    ),
                    total_utility=utility_report.total_utility,
                )
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
                        "action_outcome": action_outcome,
                        "economic_outcome": economic_outcome,
                    },
                )
                agent.remember(experience)
                self._trust_engine.update(
                    source=agent.id,
                    target=agent.id,
                    successful_interaction=action_outcome.compliant,
                )
                agent.learn(learning_experience)

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
            final_resource_level=(
                self._environment.resource_pool.available_resources
            ),
            agent_wealth={
                agent.id: agent.state.wealth
                for agent in self._agents
            },
            metrics_history=list(self._metrics_collector.history),
        )