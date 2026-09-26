"""
no_learning.py

A placeholder learner that performs no updates.
"""

from .base import LearningAlgorithm
from .experience import LearningExperience


class NoLearning(LearningAlgorithm):

    def update(
        self,
        experience: LearningExperience,
    ) -> None:
        pass