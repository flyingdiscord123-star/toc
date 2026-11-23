"""Tests for percentage-based resource regeneration."""

from __future__ import annotations

import unittest

from environment.resource_model import LinearResourceModel


class LinearResourceModelTests(unittest.TestCase):
    def test_regeneration_is_a_percentage_of_current_stock(self) -> None:
        model = LinearResourceModel(regeneration_rate=2.0)

        self.assertAlmostEqual(model.regenerate(1000.0, 1200.0), 1020.0)
        self.assertAlmostEqual(model.regenerate(500.0, 1200.0), 510.0)

    def test_regeneration_does_not_exceed_capacity(self) -> None:
        model = LinearResourceModel(regeneration_rate=10.0)

        self.assertEqual(model.regenerate(99.0, 100.0), 100.0)

    def test_zero_stock_cannot_regenerate_without_a_seed_resource(self) -> None:
        model = LinearResourceModel(regeneration_rate=10.0)

        self.assertEqual(model.regenerate(0.0, 100.0), 0.0)


if __name__ == "__main__":
    unittest.main()
