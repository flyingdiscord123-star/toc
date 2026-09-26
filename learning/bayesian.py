"""
Placeholder Bayesian learner.
"""

from .base import LearningAlgorithm
from .experience import LearningExperience


class BayesianLearning(LearningAlgorithm):

    def update(
        self,
        experience: LearningExperience,
    ) -> None:
        raise NotImplementedError(
            "Bayesian learning will be implemented later."
        )