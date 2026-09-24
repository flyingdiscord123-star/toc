"""Compliance utility component."""

from __future__ import annotations

from .component import UtilityComponent
from .context import UtilityContext


class ComplianceComponent(UtilityComponent):
    """Provide a neutral compliance score until governance signals are modeled."""

    def evaluate(
        self,
        context: UtilityContext,
    ) -> float:
        """Return 1.0 until governance penalties and taxes are modeled."""
        _ = context
        return 1.0
