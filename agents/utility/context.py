"""Immutable context shared by utility components."""

from __future__ import annotations

from dataclasses import dataclass

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState


@dataclass(frozen=True, slots=True)
class UtilityContext:
    """Inputs required to evaluate one candidate action."""

    observation: AgentObservation
    action: AgentAction
    state: AgentState
    character: Character
