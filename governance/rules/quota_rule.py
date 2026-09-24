"""
quota_rule.py

Implements a simple extraction quota.

Agents are not permitted to request more than a fixed quantity of
resources in a single action.
"""

from __future__ import annotations

from governance.context import RuleContext
from governance.result import RuleResult
from governance.rule import Rule


class QuotaRule(Rule):
    """
    Limits the maximum extraction per action.
    """

    def __init__(
        self,
        maximum_extraction: float,
    ) -> None:
        self._maximum_extraction = maximum_extraction

    @property
    def name(self) -> str:
        return "Quota Rule"

    def evaluate(
        self,
        context: RuleContext,
    ) -> RuleResult:

        if (
            context.action.extraction_amount
            > self._maximum_extraction
        ):
            return RuleResult(
                allowed=False,
                reason=(
                    f"Extraction exceeds quota "
                    f"({self._maximum_extraction})."
                ),
            )

        return RuleResult()