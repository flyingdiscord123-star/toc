"""
memory.py

Defines the memory owned by an agent.

Memory stores historical observations, actions and experiences.

Learning algorithms operate on Memory rather than directly accessing
the simulator.

This decouples learning from the rest of the architecture and allows
different learning strategies to consume the same information.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .action import AgentAction
from .experience import AgentExperience
from .observation import AgentObservation


@dataclass(slots=True)
class AgentMemory:
    """
    Stores an agent's historical interactions.

    Memory grows throughout the simulation and can later be processed
    by reinforcement learning, evolutionary methods, Bayesian models,
    or other learning algorithms.
    """

    observations: list[AgentObservation] = field(default_factory=list)

    actions: list[AgentAction] = field(default_factory=list)

    experiences: list[AgentExperience] = field(default_factory=list)

    def remember_observation(self, observation: AgentObservation) -> None:
        """Store a newly perceived observation."""
        self.observations.append(observation)

    def remember_action(self, action: AgentAction) -> None:
        """Store an executed action."""
        self.actions.append(action)

    def remember_experience(self, experience: AgentExperience) -> None:
        """Store a complete interaction with the environment."""
        self.experiences.append(experience)

    def last_observation(self) -> AgentObservation | None:
        """Return the most recent observation, if available."""
        return self.observations[-1] if self.observations else None

    def last_action(self) -> AgentAction | None:
        """Return the most recent action, if available."""
        return self.actions[-1] if self.actions else None

    def last_experience(self) -> AgentExperience | None:
        """Return the most recent experience, if available."""
        return self.experiences[-1] if self.experiences else None

    def clear(self) -> None:
        """
        Remove all stored history.

        Primarily useful for resetting experiments or beginning a new
        simulation episode.
        """
        self.observations.clear()
        self.actions.clear()
        self.experiences.clear()