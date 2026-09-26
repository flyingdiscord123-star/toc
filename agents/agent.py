"""
agent.py

Defines the core Agent class.

An Agent coordinates the major subsystems that determine its behaviour.

The Agent intentionally does not implement decision-making,
utility evaluation, or learning directly. Instead, it delegates these
responsibilities to interchangeable strategy objects.

Responsibilities
----------------
- Maintain the agent's internal state.
- Store experience in memory.
- Delegate action selection to a DecisionPolicy.
- Delegate learning to a LearningAlgorithm.
"""

from __future__ import annotations

from .action import AgentAction
from .character import Character
from .decision import DecisionPolicy
from .experience import AgentExperience
from .memory import AgentMemory
from .observation import AgentObservation
from .state import AgentState
from .utility import UtilityFunction
from learning.base import LearningAlgorithm
from learning.experience import LearningExperience


class Agent:
    """
    Represents an autonomous agent in the simulation.

    Parameters
    ----------
    agent_id:
        Unique identifier for the agent.

    state:
        Initial internal state.

    character:
        Immutable personality traits.

    memory:
        Agent memory used to store experiences.

    decision_policy:
        Strategy used to select actions.

    utility_function:
        Strategy used to evaluate utility.

    learning:
        Strategy used to update the agent from experience.
    """

    def __init__(
        self,
        agent_id: int,
        state: AgentState,
        character: Character,
        memory: AgentMemory,
        decision_policy: DecisionPolicy,
        utility_function: UtilityFunction,
        learning: LearningAlgorithm,
    ) -> None:

        self._agent_id = agent_id
        self._state = state
        self._character = character
        self._memory = memory
        self._decision_policy = decision_policy
        self._utility_function = utility_function
        self._learning = learning

    @property
    def id(self) -> int:
        """
        Unique identifier of the agent.
        """
        return self._agent_id

    @property
    def state(self) -> AgentState:
        """
        Current internal state.
        """
        return self._state

    @property
    def character(self) -> Character:
        """
        Immutable character profile.
        """
        return self._character

    @property
    def memory(self) -> AgentMemory:
        """
        Agent memory.
        """
        return self._memory

    @property
    def utility_function(self) -> UtilityFunction:
        """Utility function used to evaluate this agent's actions."""
        return self._utility_function

    def observe(
        self,
        observation: AgentObservation,
    ) -> None:
        """
        Receive an observation from the environment.

        Currently this method stores no information.
        Future versions may update the internal state or memory.
        """

        # TODO:
        # Update internal beliefs/state from the observation.

        _ = observation

    def act(
        self,
        observation: AgentObservation,
    ) -> AgentAction:
        """
        Produce an action based on the current observation.
        """

        return self._decision_policy.decide(
            observation=observation,
            state=self._state,
            character=self._character,
            utility_function=self._utility_function,
        )

    def remember(
        self,
        experience: AgentExperience,
    ) -> None:
        """
        Store an experience in memory.
        """

        self._memory.remember_experience(experience)

    def learn(
        self,
        experience: LearningExperience,
    ) -> None:
        """
        Update the learning algorithm using a new experience.
        """

        self._learning.update(experience)
    def receive_resources(
        self,
        amount: float,
    ) -> None:
        
        self._state.wealth += amount
    def reset(self) -> None:
        """
        Reset the agent for a new simulation.

        This resets the memory and learning algorithm.
        Future versions may also reset internal state if required.
        """

        self._memory.clear()
        self._learning.reset()