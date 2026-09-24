"""
result.py

Defines the outcome of evaluating a governance rule.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RuleResult:
    """
    Result returned by a governance rule.

    Attributes
    ----------
    allowed:
        Whether the action is permitted.

    reason:
        Human-readable explanation for the decision.

    metadata:
        Optional additional information produced by the rule.
    """

    allowed: bool = True

    reason: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)