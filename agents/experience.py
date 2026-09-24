"""
experience.py

Defines a single experience collected by an agent.

Experiences are immutable records describing what an agent observed,
the action it chose, and the resulting transition.

Different learning algorithms may interpret experiences differently.

- Reinforcement Learning may compute rewards.
- Evolutionary Learning may ignore experiences entirely.
- Bayesian Learning may update beliefs.
- Future algorithms may derive custom statistics.

For this reason, the experience object remains generic and does not
embed learning-specific concepts.
"""

from __future__ import annotations

from dataclasses import dataclass,field
from typing import Any

from .action import AgentAction
from .observation import AgentObservation


@dataclass(slots=True, frozen=True)
class AgentExperience:
    """
    Immutable record of one interaction with the environment.

    Parameters
    ----------
    observation:
        Observation available before choosing an action.

    action:
        Action selected by the agent.

    outcome:
        Generic outcome information produced by the environment.
        Future examples include:
            - reward
            - utility
            - extracted resources
            - taxes paid
            - penalties
            - trust updates

    next_observation:
        Observation received after the environment updates.
    """

    observation: AgentObservation

    action: AgentAction

    next_observation: AgentObservation

    outcome: dict[str, Any] = field(default_factory=dict)