"""
Placeholder extraction limit rule.
"""

from agents.action import AgentAction

from .base_rule import BaseRule


class ExtractionLimitRule(BaseRule):

    def apply(
        self,
        action: AgentAction,
    ) -> AgentAction:

        # TODO: Enforce extraction limits.

        return action