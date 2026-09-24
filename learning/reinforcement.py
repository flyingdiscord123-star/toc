"""
Placeholder reinforcement learner.
"""

from agents.experience import AgentExperience

from .base import LearningAlgorithm

Experience = AgentExperience


class ReinforcementLearning(LearningAlgorithm):

    def learn(
        self,
        experience: Experience,
    ) -> None:
        raise NotImplementedError(
            "Reinforcement learning will be implemented later."
        )