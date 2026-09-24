"""
exporter.py

Defines exporters for simulation metrics.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .collector import MetricCollector


class MetricExporter(ABC):
    """
    Abstract exporter.
    """

    @abstractmethod
    def export(
        self,
        collector: MetricCollector,
    ) -> None:
        raise NotImplementedError