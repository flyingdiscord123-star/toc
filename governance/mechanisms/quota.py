"""Quota governance mechanism adapter."""

from __future__ import annotations

from dataclasses import replace
from typing import cast

from agents.action import AgentAction
from agents.observation import AgentObservation
from environment.environment import EnvironmentSnapshot

from governance.action_outcome import ActionOutcome
from governance.context import RuleContext
from governance.engine import RuleEngine

from .base import GovernanceMechanism


class QuotaMechanism(GovernanceMechanism):
    """Adapt the existing RuleEngine quota decision to ActionOutcome."""

    def __init__(self, rule_engine: RuleEngine) -> None:
        self._rule_engine = rule_engine

    def apply(
        self,
        action: AgentAction,
        observation: AgentObservation,
        environment: EnvironmentSnapshot,
        outcome: ActionOutcome,
    ) -> ActionOutcome:
        """Apply the current quota rules without changing RuleEngine."""
        rule_result = self._rule_engine.evaluate(
            RuleContext(
                agent=cast("Agent", None),
                action=action,
                environment=environment,
            )
        )
        if rule_result.allowed:
            return outcome

        return replace(
            outcome,
            approved_extraction=0.0,
            net_resources_received=0.0,
            compliant=False,
            violation_reason=rule_result.reason,
        )
