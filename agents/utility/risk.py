"""Risk utility component."""

from __future__ import annotations

from .component import UtilityComponent
from .context import UtilityContext


class RiskComponent(UtilityComponent):
    """Score risk quadratically as the harvested quota share grows."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return normalized perceived risk from extraction size."""
        quota = context.observation.quota_limit
        if quota <= 0.0:
            return 0.0
        quota_share = context.action.extraction_amount / quota
        score = quota_share * quota_share
        return min(max(score, 0.0), 1.0)
