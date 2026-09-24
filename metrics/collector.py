"""Metrics collection architecture."""

from __future__ import annotations

from dataclasses import dataclass, field

from .round_metrics import RoundMetrics


@dataclass(slots=True)
class MetricsCollector:
    """Collects an immutable history of round-level metrics."""

    _history: list[RoundMetrics] = field(default_factory=list)

    @property
    def history(self) -> tuple[RoundMetrics, ...]:
        """Return the recorded metrics as a read-only history."""
        return tuple(self._history)

    def record(self, metrics: RoundMetrics) -> None:
        """Record one completed round."""
        self._history.append(metrics)

    def reset(self) -> None:
        """Clear all collected metrics."""
        self._history.clear()


# Backward-compatible alias retained for existing imports.
MetricCollector = MetricsCollector