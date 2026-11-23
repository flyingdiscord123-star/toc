"""Risk utility component."""

from __future__ import annotations

from .component import UtilityComponent
from .context import UtilityContext


class RiskComponent(UtilityComponent):
    """Increase risk as harvest becomes large relative to current resources."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Scale quota-normalized harvest risk by current resource scarcity."""
        environment = context.observation.environment
        quota = context.observation.quota_limit
        harvest = max(context.action.extraction_amount, 0.0)
        if quota <= 0.0 or harvest == 0.0:
            return 0.0
        current_resources = max(environment.available_resources, 1e-9)
        capacity = max(environment.maximum_capacity, 1.0)
        return (harvest / current_resources) * (capacity / quota)
