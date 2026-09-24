"""Utility-maximizing decision policy."""

from __future__ import annotations

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility import UtilityFunction

from .base import DecisionPolicy


class UtilityMaximizationPolicy(DecisionPolicy):
    """Choose the candidate action with the highest utility."""

    candidate_extraction_amounts = [0, 2, 4, 6, 8, 10]

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

        best_action = AgentAction(
            extraction_amount=self.candidate_extraction_amounts[0]
        )
        best_utility = utility_function.evaluate(
            observation=observation,
            action=best_action,
            state=state,
            character=character,
        )

        for extraction_amount in self.candidate_extraction_amounts[1:]:
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
