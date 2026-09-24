"""Deterministic seed generation for experiment runs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SeedGenerator:
	"""Generate deterministic, increasing integer seeds."""

	initial_seed: int = 42
	_next: int = field(init=False)

	def __post_init__(self) -> None:
		self._next = self.initial_seed

	def next_seed(self) -> int:
		"""Return the next deterministic seed."""
		seed = self._next
		self._next += 1
		return seed
