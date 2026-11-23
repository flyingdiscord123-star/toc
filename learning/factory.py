"""
factory.py

Factory for creating learning algorithms.
"""

from __future__ import annotations

from .base import LearningAlgorithm
from .bayesian import BayesianLearning
from .evolutionary import EvolutionaryLearning
from .gradient_utility import SVOGradientLearning
from .no_learning import NoLearning
from .reinforcement import ReinforcementLearning


class LearningFactory:
    """
    Factory responsible for constructing learning algorithms.
    """

    _ALGORITHMS = {
        "NoLearning": NoLearning,
        "Reinforcement": ReinforcementLearning,
        "Evolutionary": EvolutionaryLearning,
        "Bayesian": BayesianLearning,
        "SVOGradient": SVOGradientLearning,
    }

    @classmethod
    def create(
        cls,
        algorithm: str,
        **options: float,
    ) -> LearningAlgorithm:

        try:
            implementation = cls._ALGORITHMS[algorithm]

        except KeyError as exc:
            raise ValueError(
                f"Unknown learning algorithm '{algorithm}'."
            ) from exc

        if implementation is SVOGradientLearning:
            return implementation(**options)
        return implementation()