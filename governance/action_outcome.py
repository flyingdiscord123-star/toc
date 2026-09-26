"""Canonical consequences of one governed agent action."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ActionOutcome:
    """Immutable outcome produced by governance and environment execution."""

    requested_extraction: float
    approved_extraction: float
    net_resources_received: float
    tax_paid: float
    subsidy_received: float
    compliant: bool
    violation_reason: str | None
