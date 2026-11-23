"""Utility-maximizing decision policy."""

from __future__ import annotations

from math import ceil
from random import Random

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility import UtilityFunction
from config.simulation_config import DecisionConfig

from .base import DecisionPolicy


class UtilityMaximizationPolicy(DecisionPolicy):
    """Select a highly ranked candidate with controlled exploration."""

    def __init__(
        self,
        decision_config: DecisionConfig | None = None,
        quota_limit: float | None = 20.0,
        random_seed: int | None = None,
        rng: Random | None = None,
        num_agents: int = 1,
        harvest_fraction: float = 0.05,
        reserve_fraction: float = 0.05,
        num_candidates: int = 41,
    ) -> None:
        self._decision_config = decision_config or DecisionConfig()
        if quota_limit is not None and not 0.0 <= quota_limit <= 100.0:
            raise ValueError("quota_limit must be between 0 and 100.")
        if num_agents <= 0:
            raise ValueError("num_agents must be positive.")
        if not 0.0 <= harvest_fraction <= 1.0:
            raise ValueError("harvest_fraction must be between 0 and 1.")
        if not 0.0 <= reserve_fraction <= 1.0:
            raise ValueError("reserve_fraction must be between 0 and 1.")
        if num_candidates < 11:
            raise ValueError("num_candidates must be at least 11.")
        self._quota_limit = quota_limit
        self._num_agents = num_agents
        self._harvest_fraction = harvest_fraction
        self._reserve_fraction = reserve_fraction
        self._num_candidates = num_candidates
        self._rng = rng if rng is not None else Random(random_seed)

    def candidate_extraction_amounts(
        self,
        available_stock: float | None = None,
        maximum_capacity: float | None = None,
    ) -> list[float]:
        """Return evenly spaced candidates through the per-capita stock cap."""
        if (available_stock is None) != (maximum_capacity is None):
            raise ValueError(
                "available_stock and maximum_capacity must be provided together."
            )
        if available_stock is None or maximum_capacity is None:
            if self._quota_limit is None:
                raise ValueError(
                    "Environment stock and capacity are required when quota is disabled."
                )
            cap = self._quota_limit
        else:
            if maximum_capacity <= 0.0:
                raise ValueError("maximum_capacity must be positive.")
            reserve = self._reserve_fraction * maximum_capacity
            cap = (
                self._harvest_fraction
                * max(0.0, available_stock - reserve)
                / self._num_agents
            )
            if self._quota_limit is not None:
                cap = min(cap, self._quota_limit)
        return [
            cap * index / (self._num_candidates - 1)
            for index in range(self._num_candidates)
        ]

    @staticmethod
    def top_k_size(candidate_count: int) -> int:
        """Return ceil(50% of the candidate space)."""
        if candidate_count < 0:
            raise ValueError("candidate_count must be non-negative.")
        return ceil(0.5 * candidate_count)

    def rank_candidates(
        self,
        observation: AgentObservation,
        state: AgentState,
        character: Character,
        utility_function: UtilityFunction,
    ) -> list[tuple[AgentAction, float]]:
        """Evaluate every candidate and return actions in descending utility."""
        ranked = []
        for amount in self.candidate_extraction_amounts(
            available_stock=observation.environment.available_resources,
            maximum_capacity=observation.environment.maximum_capacity,
        ):
            action = AgentAction(extraction_amount=amount)
            ranked.append(
                (
                    action,
                    utility_function.evaluate(
                        observation=observation,
                        action=action,
                        state=state,
                        character=character,
                    ),
                )
            )
        return sorted(ranked, key=lambda item: item[1], reverse=True)

    def decide(
        self,
        observation: AgentObservation,
        state: AgentState,
        character: Character,
        utility_function: UtilityFunction | None = None,
    ) -> AgentAction:
        """Evaluate candidate extraction actions and return the best one."""
        if utility_function is None:
            raise ValueError(
                "UtilityMaximizationPolicy requires a utility function."
            )

        ranked = self.rank_candidates(
            observation=observation,
            state=state,
            character=character,
            utility_function=utility_function,
        )
        best_action = ranked[0][0]
        exploration_probability = (
            self._decision_config.exploration_probability
        )
        if (
            exploration_probability == 0.0
            or len(ranked) == 1
            or self._rng.random() >= exploration_probability
        ):
            return best_action

        top_k = self.top_k_size(len(ranked))
        exploration_candidates = ranked[1 : top_k + 1]
        no_harvest_utility = next(
            utility
            for action, utility in ranked
            if action.extraction_amount == 0.0
        )
        worthwhile_candidates = [
            (action, utility)
            for action, utility in exploration_candidates
            if utility >= no_harvest_utility
        ]
        if not worthwhile_candidates:
            return best_action
        return self._rng.choice(worthwhile_candidates)[0]
