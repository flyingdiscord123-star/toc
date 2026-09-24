"""Immutable economic accounting for one action."""

from __future__ import annotations

from dataclasses import dataclass

from governance.action_outcome import ActionOutcome


@dataclass(frozen=True, slots=True)
class EconomicOutcome:
    """Economic values applied once to an agent's wealth."""

    gross_extraction: float
    tax_paid: float
    fine_paid: float
    subsidy_received: float
    net_gain: float

    @classmethod
    def from_action_outcome(
        cls,
        outcome: ActionOutcome,
    ) -> "EconomicOutcome":
        """Create accounting values from a completed action outcome."""
        gross_extraction = outcome.net_resources_received
        net_gain = (
            gross_extraction
            - outcome.tax_paid
            - outcome.fine_paid
            + outcome.subsidy_received
        )
        return cls(
            gross_extraction=gross_extraction,
            tax_paid=outcome.tax_paid,
            fine_paid=outcome.fine_paid,
            subsidy_received=outcome.subsidy_received,
            net_gain=net_gain,
        )
