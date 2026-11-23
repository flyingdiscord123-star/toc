"""Reports explaining the SVO utility of candidate actions."""

from __future__ import annotations

from dataclasses import dataclass

from agents.action import AgentAction


@dataclass(frozen=True, slots=True)
class UtilityEvaluation:
    """Two normalized component scores and total utility."""

    action: AgentAction
    chosen_w: float
    chosen_s: float
    wealth_weight: float
    sustainability_weight: float
    total_utility: float
