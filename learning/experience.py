"""Immutable learning input for one completed agent decision."""

from __future__ import annotations

from dataclasses import dataclass

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from economics.economic_outcome import EconomicOutcome


@dataclass(frozen=True, slots=True)
class LearningExperience:
    """Describe one decision without simulation-wide state."""

    observation: AgentObservation
    chosen_action: AgentAction
    economic_outcome: EconomicOutcome
    utility_component_scores: tuple[tuple[str, float], ...]
    total_utility: float
    character: Character
    chosen_w: float
    chosen_s: float
    predicted_utility: float
    realized_reward: float
    normalization_capacity: float
