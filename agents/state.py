"""
state.py

Defines the mutable internal state of an agent.

AgentState represents everything that belongs intrinsically to an
agent and evolves throughout the simulation.

It intentionally does NOT contain observations, decisions,
personality, or learning information. Those responsibilities belong
to other modules.

The separation keeps the architecture modular and allows different
learning algorithms to operate without modifying the state model.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class AgentState:
    """
    Mutable internal state of an agent.

    Attributes
    ----------
    agent_id:
        Unique identifier for this agent.

    wealth:
        Total accumulated resources owned by the agent.

    alive:
        Whether the agent is currently active in the simulation.

    current_round:
        The latest simulation round processed by the agent.
    """

    agent_id: UUID

    wealth: float = 0.0

    alive: bool = True

    current_round: int = 0