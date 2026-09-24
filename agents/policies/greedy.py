"""Greedy decision policy."""

from __future__ import annotations

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility import UtilityFunction

from .base import DecisionPolicy


class GreedyDecisionPolicy(DecisionPolicy):
    """
    Baseline greedy policy.

    Always extracts a fixed amount.
    """

    def decide(
        self,
        observation: AgentObservation,
        state: AgentState,
        character: Character,
        utility_function: UtilityFunction | None = None,
    ) -> AgentAction:
        return AgentAction(extraction_amount=10.0)
