"""
result.py

Defines the result returned by a completed simulation.
"""

from __future__ import annotations

from dataclasses import dataclass

from metrics.round_metrics import RoundMetrics


@dataclass(slots=True)
class SimulationResult:
    """
    Stores the outcome of one simulation run.
    """

    rounds_completed: int

    final_resource_level: float

    agent_wealth: dict[int, float]

    metrics_history: list[RoundMetrics]