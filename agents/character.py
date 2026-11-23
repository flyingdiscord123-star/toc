"""SVO personality profile for an agent."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from config.simulation_config import CharacterType


@dataclass(slots=True, init=False)
class Character:
    """Mutable SVO angle with an immutable baseline profile angle."""

    character_type: CharacterType
    _theta: float
    _initial_theta: float = field(repr=False)

    def __init__(self, character_type: CharacterType, theta: float) -> None:
        self.character_type = character_type
        self.theta = theta
        self._initial_theta = theta

    @property
    def theta(self) -> float:
        """Current social value orientation angle, in radians."""
        return self._theta

    @theta.setter
    def theta(self, value: float) -> None:
        if not 0.0 <= value <= math.pi / 2:
            raise ValueError("theta must be between 0 and pi/2.")
        self._theta = value

    @property
    def initial_theta(self) -> float:
        """Original profile angle used for baseline anchoring."""
        return self._initial_theta

    @property
    def effective_weights(self) -> tuple[float, float]:
        """Return the wealth and sustainability weights."""
        return math.cos(self.theta), math.sin(self.theta)

    @classmethod
    def greedy(cls) -> "Character":
        """Create a profile focused on immediate extraction."""
        return cls(CharacterType.GREEDY, 0.0)

    @classmethod
    def cooperative(cls) -> "Character":
        """Create a sustainability-oriented wealth profile."""
        return cls(CharacterType.COOPERATIVE, math.radians(64.0))

    @classmethod
    def risk_averse(cls) -> "Character":
        """Create the profile historically named risk-averse."""
        return cls(CharacterType.RISK_AVERSE, math.radians(67.0))
