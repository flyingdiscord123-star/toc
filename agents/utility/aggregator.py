"""Pure two-component SVO utility evaluation."""

from __future__ import annotations

import math
from dataclasses import dataclass
from collections.abc import Iterable

from agents.action import AgentAction
from agents.character import Character
from agents.observation import AgentObservation
from agents.state import AgentState

from . import UtilityFunction
from .report import UtilityEvaluation


@dataclass(slots=True)
class SVOUtilityFunction(UtilityFunction):
    """Evaluate capacity-normalized wealth and concave sustainability."""

    sustainability_exponent: float = 0.85
    wealth_exponent: float = 0.92

    def __post_init__(self) -> None:
        if not 0.0 < self.wealth_exponent < 1.0:
            raise ValueError("wealth_exponent must be between 0 and 1.")
        if not 0.0 < self.sustainability_exponent < 1.0:
            raise ValueError(
                "sustainability_exponent must be between 0 and 1."
            )

    def evaluate(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> float:
        """Return the two-component utility for one candidate action."""
        return self.evaluate_report(
            observation,
            action,
            state,
            character,
        ).total_utility

    def evaluate_report(
        self,
        observation: AgentObservation,
        action: AgentAction,
        state: AgentState,
        character: Character,
    ) -> UtilityEvaluation:
        """Return normalized component values and their weighted utility."""
        _ = state
        environment = observation.environment
        if environment.maximum_capacity <= 0.0:
            raise ValueError("maximum_capacity must be positive.")
        if not 0.0 < self.wealth_exponent < 1.0:
            raise ValueError("wealth_exponent must be between 0 and 1.")
        if not 0.0 < self.sustainability_exponent < 1.0:
            raise ValueError(
                "sustainability_exponent must be between 0 and 1."
            )
        capacity = environment.maximum_capacity
        current_stock = max(environment.available_resources, 0.0)
        feasible_extraction = min(
            max(action.extraction_amount, 0.0),
            current_stock,
        )
        wealth_fraction = min(feasible_extraction / capacity, 1.0)
        chosen_w = math.pow(wealth_fraction, self.wealth_exponent)

        post_extraction_stock = current_stock - feasible_extraction
        projected_next_stock = post_extraction_stock * (
            1.0 + environment.regeneration_rate / 100.0
        )
        stock_fraction = min(
            max(projected_next_stock, 0.0),
            capacity,
        ) / capacity
        chosen_s = math.pow(stock_fraction, self.sustainability_exponent)
        wealth_weight, sustainability_weight = character.effective_weights
        total_utility = (
            wealth_weight * chosen_w
            + sustainability_weight * chosen_s
        )
        return UtilityEvaluation(
            action=action,
            chosen_w=chosen_w,
            chosen_s=chosen_s,
            wealth_weight=wealth_weight,
            sustainability_weight=sustainability_weight,
            total_utility=total_utility,
        )

    def evaluate_candidates(
        self,
        observation: AgentObservation,
        candidate_extraction_amounts: Iterable[float],
        state: AgentState,
        character: Character,
    ) -> list[UtilityEvaluation]:
        """Return evaluation reports in candidate-action order."""
        return [
            self.evaluate_report(
                observation=observation,
                action=AgentAction(extraction_amount=amount),
                state=state,
                character=character,
            )
            for amount in candidate_extraction_amounts
        ]


LinearUtilityFunction = SVOUtilityFunction
