"""Reports explaining the utility of candidate actions."""

from __future__ import annotations

from dataclasses import dataclass

from agents.action import AgentAction


@dataclass(frozen=True, slots=True)
class UtilityEvaluation:
    """Component scores and total utility for one candidate action."""

    action: AgentAction
    gain: float
    sustainability: float
    risk: float
    total_utility: float
