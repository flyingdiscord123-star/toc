"""
Placeholder Bayesian learner.
"""

from agents.experience import AgentExperience

from .base import LearningAlgorithm

Experience = AgentExperience


class BayesianLearning(LearningAlgorithm):

    def learn(
        self,
        experience: Experience,
    ) -> None:
        raise NotImplementedError(
            "Bayesian learning will be implemented later."
        )