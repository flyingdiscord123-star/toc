"""Wealth utility component."""

from __future__ import annotations

from .component import (
    MAXIMUM_CANDIDATE_EXTRACTION,
    UtilityComponent,
)
from .context import UtilityContext


class WealthComponent(UtilityComponent):
    """Score a candidate by its direct extraction payoff."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return normalized expected net reward."""
        maximum_possible_reward = MAXIMUM_CANDIDATE_EXTRACTION
        net_income = (
            context.economic_outcome.net_income
            if context.economic_outcome is not None
            else context.action.extraction_amount
        )
        score = (
            net_income / maximum_possible_reward
        )
        return min(max(score, 0.0), 1.0)
