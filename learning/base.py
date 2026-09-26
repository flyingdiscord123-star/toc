"""
base.py

Defines the abstract interface for learning algorithms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .experience import LearningExperience


class LearningAlgorithm(ABC):
    """
    Base interface for all learning algorithms.
    """

    @abstractmethod
    def update(
        self,
        experience: LearningExperience,
    ) -> None:
        """
        Update the internal model using one experience.
        """
        raise NotImplementedError

    def learn(self, experience: LearningExperience) -> None:
        """Backward-compatible alias for update()."""
        self.update(experience)

    def reset(self) -> None:
        """
        Reset the learner.

        Override if necessary.
        """
        pass