"""
Placeholder penalty rule.
"""

from agents.action import AgentAction

from .base_rule import BaseRule


class PenaltyRule(BaseRule):

    def apply(
        self,
        action: AgentAction,
    ) -> AgentAction:

        # TODO: Apply penalties.

        return action