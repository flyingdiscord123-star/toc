"""
rule.py

Defines the abstract interface implemented by every governance rule.

Rules evaluate proposed agent actions and determine whether they are
permitted or should be modified before execution.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .context import RuleContext
from .result import RuleResult


class Rule(ABC):
    """
    Base interface for all governance rules.

    Every governance mechanism should inherit from this class.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable rule name.
        """
        raise NotImplementedError

    @abstractmethod
    def evaluate(
        self,
        context: RuleContext,
    ) -> RuleResult:
        """
        Evaluate a proposed action.

        Parameters
        ----------
        context:
            Immutable information about the current simulation state.

        Returns
        -------
        RuleResult
            Decision produced by the rule.
        """
        raise NotImplementedError