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
        quota_limit: float = 20.0,
        random_seed: int | None = None,
        rng: Random | None = None,
    ) -> None:
        self._decision_config = decision_config or DecisionConfig()
        if not 0.0 <= quota_limit <= 100.0:
            raise ValueError("quota_limit must be between 0 and 100.")
        self._quota_limit = quota_limit
        self._rng = rng if rng is not None else Random(random_seed)

    def candidate_extraction_amounts(
        self,
        quota_limit: float | None = None,
    ) -> list[float]:
        """Generate integer harvest amounts from zero through the quota."""
        quota = self._quota_limit if quota_limit is None else quota_limit
        if not 0.0 <= quota <= 100.0:
            raise ValueError("quota_limit must be between 0 and 100.")
        whole_quota = int(quota)
        candidates = [float(amount) for amount in range(whole_quota + 1)]
        if quota != whole_quota:
            candidates.append(quota)
        return candidates

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
            min(self._quota_limit, observation.quota_limit)
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
        return self._rng.choice(exploration_candidates)[0]
