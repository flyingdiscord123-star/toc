"""
registry.py

Stores the governance rules that are active in a simulation.

The RuleRegistry owns the collection of enabled rules but does not
evaluate them. Rule evaluation is handled by the RuleEngine.
"""

from __future__ import annotations

from collections.abc import Iterator

from .rule import Rule


class RuleRegistry:
    """
    Stores the governance rules enabled for a simulation.
    """

    def __init__(self) -> None:
        self._rules: list[Rule] = []

    def register(
        self,
        rule: Rule,
    ) -> None:
        """
        Register a governance rule.
        """
        self._rules.append(rule)

    def unregister(
        self,
        rule: Rule,
    ) -> None:
        """
        Remove a governance rule.
        """
        self._rules.remove(rule)

    def clear(self) -> None:
        """
        Remove all registered rules.
        """
        self._rules.clear()

    @property
    def rules(self) -> tuple[Rule, ...]:
        """
        Return all registered rules.
        """
        return tuple(self._rules)

    def __iter__(self) -> Iterator[Rule]:
        """
        Iterate over all registered rules.
        """
        return iter(self._rules)

    def __len__(self) -> int:
        """
        Return the number of registered rules.
        """
        return len(self._rules)