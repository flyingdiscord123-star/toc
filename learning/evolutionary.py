"""
Placeholder evolutionary learner.
"""

from .base import LearningAlgorithm
from .experience import LearningExperience


class EvolutionaryLearning(LearningAlgorithm):

    def update(
        self,
        experience: LearningExperience,
    ) -> None:
        raise NotImplementedError(
            "Evolutionary learning will be implemented later."
        )