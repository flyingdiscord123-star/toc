"""
factories.py

Factory classes used throughout the simulator.

The simulator should never contain large if-else chains to decide
which learning algorithm, governance rule, character type, or
network topology to use.

Those decisions belong inside factories.

Current implementation only returns lightweight placeholders.

TODO (Chapter 2+):
- Construct actual Character objects.
- Construct LearningStrategy implementations.
- Construct Rule implementations.
- Construct Network topology builders.
"""

from __future__ import annotations

from dataclasses import dataclass

from .simulation_config import (
    CharacterType,
    LearningAlgorithm,
    NetworkTopology,
)


# ==========================================================
# Placeholder Classes
# ==========================================================

@dataclass(slots=True)
class CharacterPlaceholder:
    """Temporary stand-in for future Character implementations."""

    character_type: CharacterType


@dataclass(slots=True)
class LearningPlaceholder:
    """Temporary stand-in for future learning strategies."""

    algorithm: LearningAlgorithm


@dataclass(slots=True)
class RulePlaceholder:
    """Temporary stand-in for governance rule plugins."""

    rule_name: str


@dataclass(slots=True)
class TopologyPlaceholder:
    """Temporary stand-in for network topology builders."""

    topology: NetworkTopology


# ==========================================================
# Factories
# ==========================================================

class CharacterFactory:
    """
    Creates character objects.

    TODO:
        Replace placeholders with actual Character subclasses.
    """

    @staticmethod
    def create(character: CharacterType) -> CharacterPlaceholder:
        return CharacterPlaceholder(character)


class LearningFactory:
    """
    Creates learning strategy objects.

    TODO:
        Return implementations from learning/.
    """

    @staticmethod
    def create(
        algorithm: LearningAlgorithm,
    ) -> LearningPlaceholder:
        return LearningPlaceholder(algorithm)


class RuleFactory:
    """
    Creates governance rule plugins.

    TODO:
        Instantiate concrete Rule classes.
    """

    @staticmethod
    def create(rule_name: str) -> RulePlaceholder:
        return RulePlaceholder(rule_name)


class TopologyFactory:
    """
    Creates network topology builders.

    TODO:
        Return NetworkX graph generators.
    """

    @staticmethod
    def create(
        topology: NetworkTopology,
    ) -> TopologyPlaceholder:
        return TopologyPlaceholder(topology)