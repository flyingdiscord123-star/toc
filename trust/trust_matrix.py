"""
trust_matrix.py

Stores directed trust values between agents.
"""

from __future__ import annotations


class TrustMatrix:
    """
    Pairwise directed trust.

    Trust values lie in [0,1].
    """

    def __init__(self, default_trust: float = 0.5) -> None:
        self._default = default_trust
        self._trust: dict[int, dict[int, float]] = {}

    def get(
        self,
        source: int,
        target: int,
    ) -> float:
        return (
            self._trust
            .get(source, {})
            .get(target, self._default)
        )

    def set(
        self,
        source: int,
        target: int,
        value: float,
    ) -> None:

        value = max(0.0, min(1.0, value))

        self._trust.setdefault(source, {})[target] = value

    def neighbours(
        self,
        source: int,
    ) -> dict[int, float]:
        return self._trust.get(source, {})

    def average(self) -> float:
        """Return the average of explicitly stored trust values."""
        values = self._stored_values()
        return sum(values) / len(values) if values else self._default

    def minimum(self) -> float:
        """Return the minimum explicitly stored trust value."""
        values = self._stored_values()
        return min(values) if values else self._default

    def maximum(self) -> float:
        """Return the maximum explicitly stored trust value."""
        values = self._stored_values()
        return max(values) if values else self._default

    def _stored_values(self) -> list[float]:
        """Return a snapshot of explicitly stored trust values."""
        return [
            value
            for targets in self._trust.values()
            for value in targets.values()
        ]