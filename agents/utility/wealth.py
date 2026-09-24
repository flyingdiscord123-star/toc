"""Wealth utility component."""

from __future__ import annotations

from .component import UtilityComponent
from .context import UtilityContext


class WealthComponent(UtilityComponent):
    """Score a candidate by its direct extraction payoff."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return normalized expected net reward."""
        available_resources = (
            context.observation.environment.available_resources
        )
        maximum_possible_reward = max(
            available_resources,
            context.action.extraction_amount,
            1.0,
        )
        score = (
            context.action.extraction_amount / maximum_possible_reward
        )
        return min(max(score, 0.0), 1.0)
