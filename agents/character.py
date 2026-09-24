"""
character.py

Defines immutable personality characteristics for agents.

A Character describes who an agent is, not what it does.

Decision-making, learning, and utility calculations are handled by
their respective modules.
"""

from __future__ import annotations

from dataclasses import dataclass

from config.simulation_config import CharacterType

from .utility_weights import UtilityWeights


@dataclass(slots=True, frozen=True)
class Character:
    """
    Immutable personality description for an agent.

    Parameters
    ----------
    character_type:
        High-level personality category.

    utility_weights:
        Relative importance assigned to each utility component.
    """

    character_type: CharacterType

    utility_weights: UtilityWeights

    @classmethod
    def greedy(cls) -> "Character":
        """Create a character focused primarily on wealth."""
        return cls(
            character_type=CharacterType.GREEDY,
            utility_weights=UtilityWeights(
                wealth=0.85,
                sustainability=0.05,
                trust=0.05,
                compliance=0.00,
                risk=0.05,
            ),
        )

    @classmethod
    def cooperative(cls) -> "Character":
        """Create a character emphasizing sustainability and trust."""
        return cls(
            character_type=CharacterType.COOPERATIVE,
            utility_weights=UtilityWeights(
                wealth=0.35,
                sustainability=0.35,
                trust=0.20,
                compliance=0.05,
                risk=0.05,
            ),
        )

    @classmethod
    def risk_averse(cls) -> "Character":
        """Create a character with a high risk sensitivity."""
        return cls(
            character_type=CharacterType.RISK_AVERSE,
            utility_weights=UtilityWeights(
                wealth=0.35,
                sustainability=0.15,
                trust=0.10,
                compliance=0.10,
                risk=0.30,
            ),
        )
