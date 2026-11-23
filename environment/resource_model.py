"""
resource_model.py

Defines resource regeneration models.

A ResourceModel determines how the shared resource changes over time.

Different regeneration equations can be implemented without modifying
the ResourcePool or Environment.

Examples
--------
- Linear regeneration
- Logistic growth
- Seasonal regeneration
- Stochastic regeneration
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ResourceModel(ABC):
    """
    Abstract interface for resource regeneration models.
    """

    @abstractmethod
    def regenerate(
        self,
        current_resources: float,
        maximum_capacity: float,
    ) -> float:
        """
        Compute the amount of resource after regeneration.

        Parameters
        ----------
        current_resources:
            Current amount of resource.

        maximum_capacity:
            Maximum capacity of the environment.

        Returns
        -------
        float
            New resource amount.
        """
        raise NotImplementedError


class PlaceholderResourceModel(ResourceModel):
    """
    Temporary regeneration model.

    This implementation exists only to complete the architecture.
    Actual regeneration equations will be introduced in a later chapter.
    """

    def regenerate(
        self,
        current_resources: float,
        maximum_capacity: float,
    ) -> float:
        raise NotImplementedError(
            "Resource regeneration models will be implemented in a future chapter."
        )
class LinearResourceModel(ResourceModel):
    """
    Regenerate a fixed percentage of the remaining resource per round.

    ``regeneration_rate`` is expressed in percentage points, so a rate of
    ``2.0`` adds 2% of the post-harvest stock each round.
    """

    def __init__(
        self,
        regeneration_rate: float,
    ) -> None:
        self._regeneration_rate = regeneration_rate

    def regenerate(
        self,
        current_resources: float,
        maximum_capacity: float,
    ) -> float:
        regenerated = current_resources * (
            1.0 + self._regeneration_rate / 100.0
        )

        return min(regenerated, maximum_capacity)