"""
app.py

Application entry point.

For Chapter 1 this file simply creates the default simulation
configuration and constructs a Simulation instance.

No simulation logic is executed.
"""

from config.defaults import DEFAULT_SIMULATION
from simulation import Simulation


def main() -> None:
    """
    Create the default simulation configuration and display
    a brief summary.
    """

    simulation = Simulation(DEFAULT_SIMULATION)

    print("=" * 50)
    print("Commons Simulator")
    print("=" * 50)

    print(
        f"Agents: "
        f"{simulation.config.agents.num_agents}"
    )

    print(
        f"Rounds: "
        f"{simulation.config.environment.rounds}"
    )

    print(
        f"Topology: "
        f"{simulation.config.network.topology.value}"
    )

    print(
        f"Learning: "
        f"{simulation.config.learning.learning_algorithm.value}"
    )

    print(
        f"Enabled Rules: "
        f"{simulation.config.governance.enabled_rules}"
    )

    print("\nSimulation object successfully created.")
    print("Initialization is not implemented yet.")


if __name__ == "__main__":
    main()