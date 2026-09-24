"""
base_rule.py

Defines the abstract interface for governance rules.

Governance rules inspect and (eventually) modify the effects of
agent actions without changing the simulator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from agents.action import AgentAction


class BaseRule(ABC):
    """
    Abstract governance rule.
    """

    @abstractmethod
    def apply(
        self,
        action: AgentAction,
    ) -> AgentAction:
        """
        Apply this rule to an agent action.

        Current implementation is a placeholder.

        Future chapters may return a richer ActionResolution object.
        """
        raise NotImplementedError