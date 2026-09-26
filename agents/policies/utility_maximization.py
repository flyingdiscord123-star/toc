"""Utility-maximizing decision policy."""

from __future__ import annotations

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility import UtilityFunction
from config.simulation_config import DecisionConfig

from .base import DecisionPolicy


class UtilityMaximizationPolicy(DecisionPolicy):
    """Choose the candidate action with the highest utility."""

    def __init__(
        self,
        decision_config: DecisionConfig | None = None,
    ) -> None:
        self._decision_config = decision_config or DecisionConfig()

    def candidate_extraction_amounts(self) -> list[float]:
        """Generate the configured candidate extraction amounts."""
        config = self._decision_config
        candidates: list[float] = []
        current = config.minimum_extraction

        while current <= config.maximum_extraction + 1e-9:
            candidates.append(current)
            current += config.step_size

        if candidates[-1] != config.maximum_extraction:
            candidates.append(config.maximum_extraction)

        return candidates

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

        candidate_amounts = self.candidate_extraction_amounts()
        best_action = AgentAction(extraction_amount=candidate_amounts[0])
        best_utility = utility_function.evaluate(
            observation=observation,
            action=best_action,
            state=state,
            character=character,
        )

        for extraction_amount in candidate_amounts[1:]:
            action = AgentAction(extraction_amount=extraction_amount)
            utility = utility_function.evaluate(
                observation=observation,
                action=action,
                state=state,
                character=character,
            )

            if utility > best_utility:
                best_action = action
                best_utility = utility

        return best_action
