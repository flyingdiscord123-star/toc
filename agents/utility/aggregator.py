"""Linear aggregation of modular utility components."""

from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Iterable

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState

from .compliance import ComplianceComponent
from .component import UtilityComponent
from . import UtilityFunction
from .context import UtilityContext
from .risk import RiskComponent
from .report import UtilityEvaluation
from .sustainability import SustainabilityComponent
from .trust import TrustComponent
from .wealth import WealthComponent


@dataclass(slots=True)
class LinearUtilityFunction(UtilityFunction):
    """Aggregate one deterministic score from each utility component."""

    wealth: UtilityComponent = field(default_factory=WealthComponent)
    sustainability: UtilityComponent = field(
        default_factory=SustainabilityComponent
    )
    trust: UtilityComponent = field(default_factory=TrustComponent)
    compliance: UtilityComponent = field(default_factory=ComplianceComponent)
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
            UtilityContext(
                observation=observation,
                action=action,
                state=state,
                character=character,
            )
        ).total_utility

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
                UtilityContext(
                    observation=observation,
                    action=AgentAction(
                        extraction_amount=extraction_amount
                    ),
                    state=state,
                    character=character,
                )
            )
            for extraction_amount in candidate_extraction_amounts
        ]

    def _evaluate_context(
        self,
        context: UtilityContext,
    ) -> UtilityEvaluation:
        """Evaluate all components for one immutable context."""
        weights = context.character.utility_weights
        wealth_score = self.wealth.evaluate(context)
        sustainability_score = self.sustainability.evaluate(context)
        trust_score = self.trust.evaluate(context)
        compliance_score = self.compliance.evaluate(context)
        risk_score = self.risk.evaluate(context)

        total_utility = (
            weights.wealth * wealth_score
            + weights.sustainability * sustainability_score
            + weights.trust * trust_score
            + weights.compliance * compliance_score
            - weights.risk * risk_score
        )
        return UtilityEvaluation(
            action=context.action,
            wealth=wealth_score,
            sustainability=sustainability_score,
            trust=trust_score,
            compliance=compliance_score,
            risk=risk_score,
            total_utility=total_utility,
        )
