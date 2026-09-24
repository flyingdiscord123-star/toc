"""
resource_pool.py

Defines the shared renewable resource.

The ResourcePool stores the current quantity of the shared resource and
delegates regeneration behaviour to a ResourceModel.

It has no knowledge of agents, governance, learning algorithms, or the
simulation engine.

Responsibilities
----------------
- Store the current resource quantity.
- Allow extraction from the pool.
- Delegate regeneration to a ResourceModel.
- Reset to the initial state.
"""

from __future__ import annotations

from config.simulation_config import EnvironmentConfig

from .resource_model import ResourceModel


class ResourcePool:
    """
    Represents the shared renewable resource.

    Parameters
    ----------
    config:
        Configuration describing the shared resource.

    resource_model:
        Mathematical model governing resource regeneration.
    """

    def __init__(
        self,
        config: EnvironmentConfig,
        resource_model: ResourceModel,
    ) -> None:
        """
        Initialize the shared resource pool.
        """

        initial_resources = config.initial_resources
        maximum_capacity = config.maximum_capacity

        if initial_resources < 0:
            raise ValueError(
                "Initial resources cannot be negative."
            )

        if maximum_capacity <= 0:
            raise ValueError(
                "Maximum capacity must be positive."
            )

        if initial_resources > maximum_capacity:
            raise ValueError(
                "Initial resources cannot exceed maximum capacity."
            )

        self._config = config

        self._initial_resources = initial_resources
        self._maximum_capacity = maximum_capacity
        self._available_resources = initial_resources

        self._resource_model = resource_model

    @property
    def config(self) -> EnvironmentConfig:
        """
        Configuration associated with this resource pool.
        """
        return self._config

    @property
    def available_resources(self) -> float:
        """
        Current quantity of available resources.
        """
        return self._available_resources

    @property
    def maximum_capacity(self) -> float:
        """
        Maximum capacity of the resource pool.
        """
        return self._maximum_capacity

    def extract(
        self,
        amount: float,
    ) -> float:
        """
        Remove resources from the pool.

        Parameters
        ----------
        amount:
            Requested extraction amount.

        Returns
        -------
        float
            Actual quantity extracted.
        """

        if amount < 0:
            raise ValueError(
                "Extraction amount cannot be negative."
            )

        extracted = min(
            amount,
            self._available_resources,
        )

        self._available_resources -= extracted

        return extracted

    def regenerate(self) -> None:
        """
        Apply one regeneration step.

        The regeneration behaviour is delegated entirely to the
        configured ResourceModel.
        """

        self._available_resources = self._resource_model.regenerate(
            current_resources=self._available_resources,
            maximum_capacity=self._maximum_capacity,
        )

    def reset(self) -> None:
        """
        Restore the resource pool to its initial state.
        """

        self._available_resources = self._initial_resources