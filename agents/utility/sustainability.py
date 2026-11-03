"""Sustainability utility component."""

from __future__ import annotations

from .component import UtilityComponent
from .context import UtilityContext


class SustainabilityComponent(UtilityComponent):
    """Score the resource remaining after harvest and one regeneration step."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return expected resources normalized by environment capacity."""
        environment = context.observation.environment
        remaining_resources = max(
            environment.available_resources
            - context.action.extraction_amount,
            0.0,
        )
        expected_resources = (
            remaining_resources + environment.regeneration_rate
        )
        score = expected_resources / max(environment.maximum_capacity, 1.0)
        return min(max(score, 0.0), 1.0)
