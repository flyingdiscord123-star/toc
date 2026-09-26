"""
Placeholder reinforcement learner.
"""

from .base import LearningAlgorithm
from .experience import LearningExperience


class ReinforcementLearning(LearningAlgorithm):

    def update(
        self,
        experience: LearningExperience,
    ) -> None:
        raise NotImplementedError(
            "Reinforcement learning will be implemented later."
        )