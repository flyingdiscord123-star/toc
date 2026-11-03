"""Gain utility component."""

from __future__ import annotations

from .component import UtilityComponent
from .context import UtilityContext


class GainComponent(UtilityComponent):
    """Score the share of the available quota harvested."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        quota = context.observation.quota_limit
        if quota <= 0.0:
            return 0.0
        return min(max(context.action.extraction_amount / quota, 0.0), 1.0)
