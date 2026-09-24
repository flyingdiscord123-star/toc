"""Risk utility component."""

from __future__ import annotations

from .component import (
    MAXIMUM_CANDIDATE_EXTRACTION,
    UtilityComponent,
)
from .context import UtilityContext


class RiskComponent(UtilityComponent):
    """Provide a neutral risk score until risk modeling is added."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return normalized perceived risk from extraction size."""
        score = (
            context.action.extraction_amount
            / MAXIMUM_CANDIDATE_EXTRACTION
        )
        return min(max(score, 0.0), 1.0)
