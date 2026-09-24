"""Results collected from an experiment's simulation runs."""

from __future__ import annotations

from dataclasses import dataclass, field

from engine.result import SimulationResult


@dataclass(slots=True)
class ExperimentResult:
	"""Stores the results produced by an experiment."""

	results: list[SimulationResult] = field(default_factory=list)

	def number_of_runs(self) -> int:
		"""Return the number of simulation results collected."""
		return len(self.results)

	def latest(self) -> SimulationResult | None:
		"""Return the latest simulation result, if one exists."""
		if not self.results:
			return None
		return self.results[-1]
