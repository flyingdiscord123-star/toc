"""Reports explaining the utility of candidate actions."""

from __future__ import annotations

from dataclasses import dataclass

from agents.action import AgentAction


@dataclass(frozen=True, slots=True)
class UtilityEvaluation:
    """Component scores and total utility for one candidate action."""

    action: AgentAction
    wealth: float
    sustainability: float
    trust: float
    compliance: float
    risk: float
    total_utility: float
