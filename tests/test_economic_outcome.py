"""Focused tests for economic accounting outcomes."""

from __future__ import annotations

import unittest

from economics.economic_outcome import EconomicOutcome
from governance.action_outcome import ActionOutcome


class EconomicOutcomeTests(unittest.TestCase):
    def test_zero_policy_costs_preserve_gross_extraction(self) -> None:
        action_outcome = ActionOutcome(
            requested_extraction=10.0,
            approved_extraction=10.0,
            net_resources_received=10.0,
            tax_paid=0.0,
            subsidy_received=0.0,
            compliant=True,
            violation_reason=None,
        )

        economic_outcome = EconomicOutcome.from_action_outcome(
            action_outcome
        )

        self.assertEqual(economic_outcome.gross_income, 10.0)
        self.assertEqual(economic_outcome.net_income, 10.0)

    def test_outcome_is_immutable(self) -> None:
        outcome = EconomicOutcome(
            gross_income=10.0,
            tax_paid=0.0,
            net_income=10.0,
        )

        with self.assertRaises(AttributeError):
            outcome.net_income = 5.0  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
