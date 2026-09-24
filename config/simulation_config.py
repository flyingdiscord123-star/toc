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
        if self.initial_resources < 0:
            raise ValueError("initial_resources must be >= 0.")

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

    greedy_percentage: float
    cooperative_percentage: float
    risk_averse_percentage: float

    def __post_init__(self) -> None:

        if self.num_agents <= 0:
            raise ValueError("num_agents must be positive.")

        percentages = [
            self.greedy_percentage,
            self.cooperative_percentage,
            self.risk_averse_percentage,
        ]

        for value in percentages:
            if value < 0:
                raise ValueError("Agent percentages must be non-negative.")

        if abs(sum(percentages) - 100.0) > 1e-6:
            raise ValueError(
                "greedy_percentage + cooperative_percentage + "
                "risk_averse_percentage must equal 100."
            )


# ==========================================================
# Governance
# ==========================================================

@dataclass(frozen=True, slots=True)
class QuotaConfig:
    """Researcher-selected configuration for the quota institution."""

    enabled: bool = True
    maximum_extraction: float = 20.0


@dataclass(frozen=True, slots=True)
class TaxConfig:
    """Researcher-selected tax settings reserved for future governance."""

    enabled: bool = False
    rate: float = 0.0


@dataclass(frozen=True, slots=True)
class FineConfig:
    """Researcher-selected fine settings reserved for future governance."""

    enabled: bool = False
    amount: float = 0.0


@dataclass(frozen=True, slots=True)
class SubsidyConfig:
    """Researcher-selected subsidy settings reserved for future governance."""

    enabled: bool = False
    rate: float = 0.0


@dataclass(slots=True)
class GovernanceConfig:
    """
    Stores the exogenous institutions selected before simulation begins.

    Governance is exogenous: these institutional parameters are selected by
    the researcher before a simulation begins.

    ``enabled_rules`` is retained for compatibility with older callers.
    """

    enabled_rules: List[str] = field(default_factory=list)
    quota_enabled: bool = True
    quota_limit: float = 20.0
    tax_enabled: bool = False
    tax_rate: float = 0.0
    fine_enabled: bool = False
    fine_amount: float = 0.0

    def __post_init__(self) -> None:
        if self.quota_limit < 0:
            raise ValueError("quota_limit must be >= 0.")
        if not 0.0 <= self.tax_rate <= 1.0:
            raise ValueError("tax_rate must be between 0 and 1.")
        if self.fine_amount < 0:
            raise ValueError("fine_amount must be >= 0.")


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