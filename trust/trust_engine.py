"""
trust_engine.py

High-level interface for managing trust relationships.

The TrustEngine coordinates trust storage and trust update
strategies. The rest of the simulator should only interact
with this class.
"""

from __future__ import annotations

from .trust_matrix import TrustMatrix
from .trust_update import TrustUpdateStrategy


class TrustEngine:
    """
    Coordinates trust storage and updates.
    """

    def __init__(
        self,
        matrix: TrustMatrix,
        updater: TrustUpdateStrategy,
    ) -> None:
        self._matrix = matrix
        self._updater = updater

    def get_trust(
        self,
        source: int,
        target: int,
    ) -> float:
        """
        Return the current trust value.
        """
        return self._matrix.get(source, target)

    def update(
        self,
        source: int,
        target: int,
        successful_interaction: bool,
    ) -> None:
        """
        Update trust after an interaction.
        """

        current = self._matrix.get(source, target)

        updated = self._updater.update(
            current_trust=current,
            successful_interaction=successful_interaction,
        )

        self._matrix.set(
            source,
            target,
            updated,
        )

    def neighbours(
        self,
        source: int,
    ) -> dict[int, float]:
        """
        Return all trust values held by one agent.
        """
        return self._matrix.neighbours(source)

    def average_trust(self) -> float:
        """Return the current average trust without modifying state."""
        return self._matrix.average()

    def minimum_trust(self) -> float:
        """Return the current minimum trust without modifying state."""
        return self._matrix.minimum()

    def maximum_trust(self) -> float:
        """Return the current maximum trust without modifying state."""
        return self._matrix.maximum()