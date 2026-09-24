"""
base.py

Defines the abstract interface for learning algorithms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from agents.experience import AgentExperience

Experience = AgentExperience


class LearningAlgorithm(ABC):
    """
    Base interface for all learning algorithms.
    """

    @abstractmethod
    def learn(
        self,
        experience: Experience,
    ) -> None:
        """
        Update the internal model using one experience.
        """
        raise NotImplementedError

    def reset(self) -> None:
        """
        Reset the learner.

        Override if necessary.
        """
        pass