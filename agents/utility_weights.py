"""Relative weights used by utility-based agent architectures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UtilityWeights:
    """Relative importance assigned to each utility component."""

    gain: float
    sustainability: float
    risk: float
