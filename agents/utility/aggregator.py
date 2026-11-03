"""Linear aggregation of modular utility components."""

from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Iterable

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState

from .component import UtilityComponent
from . import UtilityFunction
from .context import UtilityContext
from .gain import GainComponent
from .risk import RiskComponent
from .report import UtilityEvaluation
from .sustainability import SustainabilityComponent


@dataclass(slots=True)
class LinearUtilityFunction(UtilityFunction):
    """Aggregate gain, sustainability, and risk using character weights."""

    gain: UtilityComponent = field(default_factory=GainComponent)
    sustainability: UtilityComponent = field(
        default_factory=SustainabilityComponent
    )
    risk: UtilityComponent = field(default_factory=RiskComponent)

    def evaluate(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> float:
        """Return the weighted utility for a candidate action."""
        return self._evaluate_context(
            observation=observation,
            action=action,
            state=state,
            character=character,
        ).total_utility

    def evaluate_report(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> UtilityEvaluation:
        """Return the component breakdown for one candidate action."""
        return self._evaluate_context(
            observation=observation,
            action=action,
            state=state,
            character=character,
        )

    def evaluate_candidates(
        self,
        observation: AgentObservation,
        candidate_extraction_amounts: Iterable[float],
        state: AgentState,
        character: Character,
    ) -> list[UtilityEvaluation]:
        """Return component reports in the order of candidate actions."""
        return [
            self._evaluate_context(
                observation=observation,
                action=AgentAction(
                    extraction_amount=extraction_amount
                ),
                state=state,
                character=character,
            )
            for extraction_amount in candidate_extraction_amounts
        ]

    def _evaluate_context(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> UtilityEvaluation:
        """Evaluate all three components for one immutable context."""
        context = UtilityContext(
            observation=observation,
            action=action,
            state=state,
            character=character,
        )
        weights = context.character.utility_weights
        gain_score = self.gain.evaluate(context)
        sustainability_score = self.sustainability.evaluate(context)
        risk_score = self.risk.evaluate(context)

        total_utility = (
            weights.gain * gain_score
            + weights.sustainability * sustainability_score
            - weights.risk * risk_score
        )
        return UtilityEvaluation(
            action=context.action,
            gain=gain_score,
            sustainability=sustainability_score,
            risk=risk_score,
            total_utility=total_utility,
        )
