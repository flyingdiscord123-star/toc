"""Experiment orchestration architecture."""

from __future__ import annotations

from config.simulation_config import SimulationConfig
from simulation import Simulation

from .experiment_result import ExperimentResult
from .seeds import SeedGenerator


class Experiment:
	"""Defines a repeatable collection of simulation runs."""

	def __init__(self, config: SimulationConfig) -> None:
		self._config = config
		self._seed_generator = SeedGenerator()

	def run(self, number_of_runs: int) -> ExperimentResult:
		"""Run a fresh configured simulation for each requested run.

		The generated seed will be applied when ``Simulation`` exposes
		deterministic seed support.
		"""
		results = []

		for _ in range(number_of_runs):
			seed = self._seed_generator.next_seed()
			# Apply ``seed`` when Simulation exposes deterministic seed support.
			_ = seed

			simulation = Simulation(self._config)

			try:
				simulation.initialize()
				simulation_result = simulation.run()
			except NotImplementedError as error:
				raise NotImplementedError(
					"Experiment.run() is ready, but Simulation has not yet "
					"been implemented."
				) from error

			results.append(simulation_result)

		return ExperimentResult(results)
