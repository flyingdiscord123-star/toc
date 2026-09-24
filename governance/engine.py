"""
engine.py

Evaluates governance rules.

The RuleEngine is responsible for executing every registered rule
against a proposed agent action.

It contains no governance logic itself. All behaviour lives inside
individual Rule implementations.
"""

from __future__ import annotations

from .context import RuleContext
from .registry import RuleRegistry
from .result import RuleResult


class RuleEngine:
    """
    Executes governance rules.

    Rules are evaluated sequentially in the order they were
    registered.
    """

    def __init__(
        self,
        registry: RuleRegistry,
    ) -> None:
        self._registry = registry

    @property
    def registry(self) -> RuleRegistry:
        """
        Return the registered governance rules.
        """
        return self._registry

    def evaluate(
        self,
        context: RuleContext,
    ) -> RuleResult:
        """
        Evaluate all registered governance rules.

        Parameters
        ----------
        context:
            Information about the proposed action.

        Returns
        -------
        RuleResult
            The final decision.
        """

        for rule in self._registry:

            result = rule.evaluate(context)

            if not result.allowed:
                return result

        return RuleResult()