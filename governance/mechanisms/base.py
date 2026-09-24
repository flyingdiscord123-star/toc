"""Common interface for composable governance mechanisms."""

from __future__ import annotations

from abc import ABC, abstractmethod

from agents.action import AgentAction
from agents.observation import AgentObservation
from environment.environment import EnvironmentSnapshot

from governance.action_outcome import ActionOutcome


class GovernanceMechanism(ABC):
    """Apply one governance transformation to an action outcome."""

    @abstractmethod
    def apply(
        self,
        action: AgentAction,
        observation: AgentObservation,
        environment: EnvironmentSnapshot,
        outcome: ActionOutcome,
    ) -> ActionOutcome:
        """Return the outcome after applying this mechanism."""
        raise NotImplementedError
