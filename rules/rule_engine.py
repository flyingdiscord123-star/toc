"""
rule_engine.py

Coordinates the execution of governance rules.
"""

from __future__ import annotations

from agents.action import AgentAction

from .base_rule import BaseRule


class RuleEngine:
    """
    Applies governance rules sequentially.
    """

    def __init__(
        self,
        rules: list[BaseRule],
    ) -> None:
        self._rules = rules

    def apply(
        self,
        action: AgentAction,
    ) -> AgentAction:
        """
        Apply all enabled rules.
        """

        for rule in self._rules:
            action = rule.apply(action)

        return action