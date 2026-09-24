"""Statistical analysis architecture for experiment results."""

from __future__ import annotations

from collections.abc import Sequence


class Statistics:
	"""Placeholder for statistical calculations over experiment results."""

	def mean(self, values: Sequence[float]) -> float:
		"""Return the mean of a sequence of values."""
		raise NotImplementedError

	def variance(self, values: Sequence[float]) -> float:
		"""Return the variance of a sequence of values."""
		raise NotImplementedError
