"""
defaults.py

Default configuration objects used throughout the simulator.

These defaults provide a convenient starting point for
experiments while remaining fully replaceable by frontend
configuration in future versions.
"""

from .simulation_config import (
    AgentConfig,
    EnvironmentConfig,
    GovernanceConfig,
    LearningAlgorithm,
    LearningConfig,
    NetworkConfig,
    NetworkTopology,
    SimulationConfig,
)


# ==========================================================
# Environment Defaults
# ==========================================================

DEFAULT_ENVIRONMENT = EnvironmentConfig(
    initial_resources=1000.0,
    maximum_capacity=1000.0,
    regeneration_rate=0.05,
    rounds=100,
)


# ==========================================================
# Network Defaults
# ==========================================================

DEFAULT_NETWORK = NetworkConfig(
    topology=NetworkTopology.SMALL_WORLD,
    average_degree=4,
    rewiring_probability=0.1,
    random_seed=42,
)


# ==========================================================
# Agent Defaults
# ==========================================================

DEFAULT_AGENTS = AgentConfig(
    num_agents=100,
    percentage_greedy=25.0,
    percentage_cooperative=25.0,
    percentage_risk_averse=25.0,
    percentage_opportunist=25.0,
)


# ==========================================================
# Governance Defaults
# ==========================================================

DEFAULT_GOVERNANCE = GovernanceConfig(
    enabled_rules=[]
)


# ==========================================================
# Learning Defaults
# ==========================================================

DEFAULT_LEARNING = LearningConfig(
    learning_algorithm=LearningAlgorithm.NO_LEARNING
)


# ==========================================================
# Simulation Defaults
# ==========================================================

DEFAULT_SIMULATION = SimulationConfig(
    environment=DEFAULT_ENVIRONMENT,
    network=DEFAULT_NETWORK,
    agents=DEFAULT_AGENTS,
    governance=DEFAULT_GOVERNANCE,
    learning=DEFAULT_LEARNING,
)