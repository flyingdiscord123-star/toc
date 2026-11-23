"""Sustainability utility component."""

from __future__ import annotations

from math import sqrt

from .component import UtilityComponent
from .context import UtilityContext


class SustainabilityComponent(UtilityComponent):
    """Reward remaining resources with increasing sensitivity near depletion."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return the square root of the remaining resource fraction."""
        environment = context.observation.environment
        remaining_resources = max(
            environment.available_resources
            - context.action.extraction_amount,
            0.0,
        )
        remaining_fraction = remaining_resources / max(
            environment.maximum_capacity,
            1.0,
        )
        return sqrt(min(max(remaining_fraction, 0.0), 1.0))
