"""
context.py

Defines the information supplied to governance rules.

Rules operate only on this immutable context rather than accessing
the simulator directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents.action import AgentAction
    from agents.agent import Agent
    from environment.environment import EnvironmentSnapshot


@dataclass(slots=True, frozen=True)
class RuleContext:
    """
    Immutable context supplied to governance rules.

    Parameters
    ----------
    agent:
        Agent requesting the action.

    action:
        Proposed action.

    environment:
        Snapshot of the current environment.
    """

    agent: "Agent"

    action: "AgentAction"

    environment: "EnvironmentSnapshot"