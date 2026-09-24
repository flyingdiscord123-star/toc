"""
simulation_config.py

Central configuration definitions for the Commons Simulator.

Every simulation should be reproducible from a single
SimulationConfig object.

Future React/FastAPI frontend will serialize directly into these
dataclasses.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


# ==========================================================
# Enums
# ==========================================================

class NetworkTopology(Enum):
    """Supported network topologies."""

    COMPLETE = "complete"
    RING = "ring"
    RANDOM = "random"
    SMALL_WORLD = "small_world"
    SCALE_FREE = "scale_free"


class LearningAlgorithm(Enum):
    """Supported learning algorithms."""

    NO_LEARNING = "NoLearning"
    EVOLUTIONARY = "Evolutionary"
    REINFORCEMENT = "Reinforcement"
    BAYESIAN = "Bayesian"
    GNN = "GNN"


class CharacterType(Enum):
    """Supported agent personality archetypes."""

    GREEDY = "greedy"
    COOPERATIVE = "cooperative"
    RISK_AVERSE = "risk_averse"
    OPPORTUNIST = "opportunist"

# ==========================================================
# Environment
# ==========================================================

@dataclass(slots=True)
class EnvironmentConfig:
    """
    Configuration describing the shared renewable resource.
    """

    initial_resources: float
    maximum_capacity: float
    regeneration_rate: float
    rounds: int

    def __post_init__(self) -> None:
        if self.initial_resources <= 0:
            raise ValueError("initial_resources must be > 0.")

        if self.maximum_capacity <= 0:
            raise ValueError("maximum_capacity must be > 0.")

        if self.maximum_capacity < self.initial_resources:
            raise ValueError(
                "maximum_capacity must be >= initial_resources."
            )

        if self.regeneration_rate < 0:
            raise ValueError(
                "regeneration_rate cannot be negative."
            )

        if self.rounds <= 0:
            raise ValueError("rounds must be positive.")


# ==========================================================
# Network
# ==========================================================

@dataclass(slots=True)
class NetworkConfig:
    """
    Configuration of the interaction network.
    """

    topology: NetworkTopology

    average_degree: int = 4
    rewiring_probability: float = 0.1
    random_seed: int | None = None

    def __post_init__(self) -> None:

        if self.average_degree < 0:
            raise ValueError(
                "average_degree cannot be negative."
            )

        if not 0 <= self.rewiring_probability <= 1:
            raise ValueError(
                "rewiring_probability must be between 0 and 1."
            )


# ==========================================================
# Agent Population
# ==========================================================

@dataclass(slots=True)
class AgentConfig:
    """
    Configuration describing the population composition.
    """

    num_agents: int

    percentage_greedy: float
    percentage_cooperative: float
    percentage_risk_averse: float
    percentage_opportunist: float

    def __post_init__(self) -> None:

        if self.num_agents <= 0:
            raise ValueError("num_agents must be positive.")

        percentages = [
            self.percentage_greedy,
            self.percentage_cooperative,
            self.percentage_risk_averse,
            self.percentage_opportunist,
        ]

        for value in percentages:
            if value < 0 or value > 100:
                raise ValueError(
                    "Percentages must lie between 0 and 100."
                )

        if abs(sum(percentages) - 100.0) > 1e-6:
            raise ValueError(
                "Agent percentages must sum to exactly 100."
            )


# ==========================================================
# Governance
# ==========================================================

@dataclass(slots=True)
class GovernanceConfig:
    """
    Stores which governance plugins are enabled.

    Rules themselves are implemented elsewhere.
    """

    enabled_rules: List[str] = field(default_factory=list)


# ==========================================================
# Learning
# ==========================================================

@dataclass(slots=True)
class LearningConfig:
    """
    Specifies which learning module should be used.

    Actual learning implementations live in learning/.
    """

    learning_algorithm: LearningAlgorithm = (
        LearningAlgorithm.NO_LEARNING
    )


# ==========================================================
# Root Configuration
# ==========================================================

@dataclass(slots=True)
class SimulationConfig:
    """
    Root configuration object.

    Every simulator component should receive this object
    (or a relevant subsection) rather than individual
    parameters.

    This keeps the architecture clean and frontend-friendly.
    """

    environment: EnvironmentConfig
    network: NetworkConfig
    agents: AgentConfig
    governance: GovernanceConfig
    learning: LearningConfig