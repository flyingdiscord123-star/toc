"""
Placeholder taxation rule.
"""

from agents.action import AgentAction

from .base_rule import BaseRule


class TaxRule(BaseRule):

    def apply(
        self,
        action: AgentAction,
    ) -> AgentAction:

        # TODO: Apply taxation.

        return action