"""
base.py

Defines decision-making interfaces for agents.

Decision policies determine which action an agent should take based
on its current observation, internal state, and personality.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState
from agents.utility import UtilityFunction


class DecisionPolicy(ABC):
    """
    Abstract interface for agent decision-making.

    The Agent delegates action selection to an implementation of this
    interface.
    """

    @abstractmethod
    def decide(
        self,
        observation: AgentObservation,
        state: AgentState,
        character: Character,
        utility_function: UtilityFunction | None = None,
    ) -> AgentAction:
        """
        Produce an action for the current timestep.
        """
        raise NotImplementedError


class PlaceholderDecisionPolicy(DecisionPolicy):
    """Placeholder implementation used until real decision policies are introduced."""

    def decide(
        self,
        observation: AgentObservation,
        state: AgentState,
        character: Character,
        utility_function: UtilityFunction | None = None,
    ) -> AgentAction:
        raise NotImplementedError(
            "Decision policies will be implemented in a future chapter."
        )
