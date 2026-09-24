"""Trust utility component."""

from __future__ import annotations

from .component import (
    MAXIMUM_CANDIDATE_EXTRACTION,
    UtilityComponent,
)
from .context import UtilityContext


class TrustComponent(UtilityComponent):
    """Provide a neutral trust score until trust is supplied to utility evaluation."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return a normalized score that favors smaller extraction."""
        normalized_extraction = (
            context.action.extraction_amount
            / MAXIMUM_CANDIDATE_EXTRACTION
        )
        return min(max(1.0 - normalized_extraction, 0.0), 1.0)
