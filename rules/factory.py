"""
factory.py

Creates governance rules from configuration.
"""

from __future__ import annotations

from .base_rule import BaseRule
from .extraction_limit import ExtractionLimitRule
from .penalty import PenaltyRule
from .tax import TaxRule


class RuleFactory:
    """
    Factory for governance rules.
    """

    _RULES = {
        "extraction_limit": ExtractionLimitRule,
        "flat_tax": TaxRule,
        "penalty": PenaltyRule,
    }

    @classmethod
    def create(
        cls,
        name: str,
    ) -> BaseRule:

        try:
            return cls._RULES[name]()

        except KeyError as exc:
            raise ValueError(
                f"Unknown rule '{name}'."
            ) from exc