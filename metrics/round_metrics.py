"""Round-level metrics snapshot."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoundMetrics:
    """Immutable metrics for a single simulation round."""

    round_number: int
    resource_level: float
    average_wealth: float
    total_wealth: float
    average_trust: float
    violations: int
    successful_extractions: int
