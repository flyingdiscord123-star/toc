"""
Placeholder evolutionary learner.
"""

from agents.experience import AgentExperience

from .base import LearningAlgorithm

Experience = AgentExperience


class EvolutionaryLearning(LearningAlgorithm):

    def learn(
        self,
        experience: Experience,
    ) -> None:
        raise NotImplementedError(
            "Evolutionary learning will be implemented later."
        )