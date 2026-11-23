"""Single-parameter gradient learning for SVO utility."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .base import LearningAlgorithm
from .experience import LearningExperience


@dataclass(slots=True)
class SVOGradientLearning(LearningAlgorithm):
    """Update an agent's SVO angle from normalized prediction error."""

    learning_rate: float = 0.01
    anchor_lambda: float = 0.20

    def __post_init__(self) -> None:
        if self.learning_rate < 0.0:
            raise ValueError("learning_rate must be non-negative.")
        if not 0.0 <= self.anchor_lambda <= 1.0:
            raise ValueError("anchor_lambda must be between 0 and 1.")

    def update(self, experience: LearningExperience) -> None:
        """Apply one analytical gradient step and baseline anchoring."""
        if experience.normalization_capacity <= 0.0:
            raise ValueError("normalization_capacity must be positive.")

        theta = experience.character.theta
        realized_norm = (
            experience.realized_reward / experience.normalization_capacity
        )
        td_error = realized_norm - experience.predicted_utility
        grad_theta = (
            -math.sin(theta) * experience.chosen_w
            + math.cos(theta) * experience.chosen_s
        )
        clamped_theta = min(
            max(
                theta + self.learning_rate * td_error * grad_theta,
                0.0,
            ),
            math.pi / 2,
        )
        experience.character.theta = (
            (1.0 - self.anchor_lambda) * clamped_theta
            + self.anchor_lambda * experience.character.initial_theta
        )


GradientUtilityLearning = SVOGradientLearning
