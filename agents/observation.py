"""
observation.py

Defines what an agent perceives during a single simulation round.

Observations are immutable snapshots of the environment and are
consumed by decision-making and learning components.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment.environment import EnvironmentSnapshot
@dataclass(slots=True, frozen=True)
class NeighborObservation:
    """
    Information visible about one neighboring agent.
    """

    agent_id: int

    wealth: float

    alive: bool
@dataclass(slots=True, frozen=True)
class AgentObservation:
    """
    Immutable observation available to an agent.

    Parameters
    ----------
    round_number:
        Current simulation round.

    available_resource:
        Current amount of resource in the shared pool.

    neighbour_ids:
        IDs of neighbouring agents.

    governance_signals:
        Information broadcast by governance mechanisms.

    metadata:
        Additional extensible information for future research.
    """

    round_number: int

    environment: "EnvironmentSnapshot"

    neighbors: tuple[NeighborObservation, ...] = ()
    governance_signals: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)
