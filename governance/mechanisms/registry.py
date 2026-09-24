"""Ordered registry for composable governance mechanisms."""

from __future__ import annotations

from collections.abc import Iterator

from agents.action import AgentAction
from agents.observation import AgentObservation
from environment.environment import EnvironmentSnapshot

from governance.action_outcome import ActionOutcome

from .base import GovernanceMechanism


class GovernanceMechanismRegistry:
    """Store and apply governance mechanisms in registration order."""

    def __init__(self) -> None:
        self._mechanisms: list[GovernanceMechanism] = []

    def register(self, mechanism: GovernanceMechanism) -> None:
        """Register a mechanism at the end of the pipeline."""
        self._mechanisms.append(mechanism)

    def unregister(self, mechanism: GovernanceMechanism) -> None:
        """Remove a registered mechanism."""
        self._mechanisms.remove(mechanism)

    def clear(self) -> None:
        """Remove all registered mechanisms."""
        self._mechanisms.clear()

    def mechanisms(self) -> tuple[GovernanceMechanism, ...]:
        """Return mechanisms in application order."""
        return tuple(self._mechanisms)

    def apply_all(
        self,
        action: AgentAction,
        observation: AgentObservation,
        environment: EnvironmentSnapshot,
        outcome: ActionOutcome,
    ) -> ActionOutcome:
        """Apply every registered mechanism sequentially."""
        for mechanism in self._mechanisms:
            outcome = mechanism.apply(
                action=action,
                observation=observation,
                environment=environment,
                outcome=outcome,
            )
        return outcome

    def __iter__(self) -> Iterator[GovernanceMechanism]:
        """Iterate over mechanisms in application order."""
        return iter(self._mechanisms)

    def __len__(self) -> int:
        """Return the number of registered mechanisms."""
        return len(self._mechanisms)
