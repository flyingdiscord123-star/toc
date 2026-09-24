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
        score = (
            context.action.extraction_amount / maximum_possible_reward
        )
        return min(max(score, 0.0), 1.0)
