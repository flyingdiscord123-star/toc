"""Simulation-level metric aggregation."""

from __future__ import annotations

from dataclasses import dataclass, field

from .round_metrics import RoundMetrics


@dataclass(slots=True)
class SimulationMetrics:
    """Container for the per-round metric history."""

    rounds: list[RoundMetrics] = field(default_factory=list)

    def add_round(
        self,
        round_number: int,
        resource_level: float,
        average_wealth: float,
        total_wealth: float,
        average_trust: float,
        violations: int,
        successful_extractions: int,
    ) -> None:
        """Append a new round metric snapshot."""
        self.rounds.append(
            RoundMetrics(
                round_number=round_number,
                resource_level=resource_level,
                average_wealth=average_wealth,
                total_wealth=total_wealth,
                average_trust=average_trust,
                violations=violations,
                successful_extractions=successful_extractions,
            )
        )

    def number_of_rounds(self) -> int:
        """Return the number of recorded rounds."""
        return len(self.rounds)

    def latest(self) -> RoundMetrics | None:
        """Return the most recent round metrics, if any."""
        if not self.rounds:
            return None
        return self.rounds[-1]
