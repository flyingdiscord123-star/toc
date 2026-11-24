"""Economic consequences of one candidate action."""

from __future__ import annotations

from dataclasses import dataclass

from governance.action_outcome import ActionOutcome


@dataclass(frozen=True, slots=True)
class EconomicOutcome:
    """Immutable gross and net income."""

    gross_income: float
    net_income: float

    @classmethod
    def create(
        cls,
        gross_income: float,
    ) -> "EconomicOutcome":
        """Create an outcome whose net income equals gross income."""
        return cls(
            gross_income=gross_income,
            net_income=gross_income,
        )

    @classmethod
    def from_action_outcome(
        cls,
        outcome: ActionOutcome,
    ) -> "EconomicOutcome":
        """Create economic accounting from a governed action outcome."""
        return cls.create(
            gross_income=outcome.net_resources_received,
        )
