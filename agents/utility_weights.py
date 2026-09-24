"""Relative weights used by utility-based agent architectures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UtilityWeights:
    """Relative importance assigned to each utility component."""

    wealth: float
    sustainability: float
    trust: float
    compliance: float
    risk: float
