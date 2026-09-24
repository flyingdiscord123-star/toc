"""
environment.py

Defines the shared simulation environment.

The Environment represents the world in which agents interact.
Its responsibility is to coordinate the shared ResourcePool and expose
immutable snapshots of the environment.

The Environment intentionally knows nothing about:

- agents
- learning algorithms
- governance rules
- the simulation engine

Those responsibilities belong to other modules.
"""

from __future__ import annotations

from dataclasses import dataclass

from .resource_pool import ResourcePool


@dataclass(slots=True, frozen=True)
class EnvironmentSnapshot:
    """
    Immutable snapshot of the observable environment.

    This snapshot is used to construct AgentObservation objects.
    Since it is immutable, agents cannot accidentally modify the
    environment.

    Parameters
    ----------
    round_number:
        Current simulation round.

    available_resources:
        Quantity of resources currently available.
    """

    round_number: int

    available_resources: float

    maximum_capacity: float = 1.0

    regeneration_rate: float = 0.0


class Environment:
    """
    Represents the shared simulation environment.

    The Environment coordinates a ResourcePool and maintains the
    current simulation round.

    It intentionally delegates all resource management to the
    ResourcePool.
    """

    def __init__(
        self,
        resource_pool: ResourcePool,
    ) -> None:
        """
        Initialize the environment.
        """

        self._resource_pool = resource_pool

        self._round_number = 0

    @property
    def round_number(self) -> int:
        """
        Current simulation round.
        """
        return self._round_number

    @property
    def resource_pool(self) -> ResourcePool:
        """
        Access the shared resource pool.

        This property exists primarily for the simulation engine,
        which is responsible for applying agent actions.
        """
        return self._resource_pool

    def snapshot(self) -> EnvironmentSnapshot:
        """
        Return an immutable snapshot of the current environment.
        """

        return EnvironmentSnapshot(
            round_number=self._round_number,
            available_resources=self._resource_pool.available_resources,
            maximum_capacity=self._resource_pool.maximum_capacity,
            regeneration_rate=self._resource_pool.config.regeneration_rate,
        )

    def step(self) -> None:
        """
        Advance the environment by one timestep.

        The Environment itself does not implement regeneration.
        Instead, it delegates regeneration to the ResourcePool.
        """

        self._resource_pool.regenerate()

        self._round_number += 1

    def reset(self) -> None:
        """
        Reset the environment to its initial state.
        """

        self._resource_pool.reset()

        self._round_number = 0