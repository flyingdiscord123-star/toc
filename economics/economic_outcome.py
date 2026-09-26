"""Economic consequences of one candidate action."""

from __future__ import annotations

from dataclasses import dataclass

from governance.action_outcome import ActionOutcome


@dataclass(frozen=True, slots=True)
class EconomicOutcome:
    """Immutable income, tax cost, and resulting net income."""

    gross_income: float
    tax_paid: float
    net_income: float

    @classmethod
    def create(
        cls,
        gross_income: float,
        tax_paid: float,
    ) -> "EconomicOutcome":
        """Create an outcome whose net income follows the accounting rule."""
        return cls(
            gross_income=gross_income,
            tax_paid=tax_paid,
            net_income=gross_income - tax_paid,
        )

    @classmethod
    def from_action_outcome(
        cls,
        outcome: ActionOutcome,
    ) -> "EconomicOutcome":
        """Create economic accounting from a governed action outcome."""
        return cls.create(
            gross_income=outcome.net_resources_received,
            tax_paid=outcome.tax_paid,
        )
