"""
no_learning.py

A placeholder learner that performs no updates.
"""

from agents.experience import AgentExperience

from .base import LearningAlgorithm

Experience = AgentExperience


class NoLearning(LearningAlgorithm):

    def learn(
        self,
        experience: Experience,
    ) -> None:
        pass