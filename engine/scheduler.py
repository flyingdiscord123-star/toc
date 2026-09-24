"""
scheduler.py

Defines scheduling strategies for agent execution.

Schedulers determine the order in which agents are given the
opportunity to act during a simulation round.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from agents.agent import Agent


class Scheduler(ABC):
    """
    Abstract scheduler interface.
    """

    @abstractmethod
    def order(
        self,
        agents: list[Agent],
    ) -> list[Agent]:
        """
        Return the order in which agents should act.
        """
        raise NotImplementedError


class SequentialScheduler(Scheduler):
    """
    Executes agents in the order they were created.
    """

    def order(
        self,
        agents: list[Agent],
    ) -> list[Agent]:
        return agents