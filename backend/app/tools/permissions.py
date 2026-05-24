from __future__ import annotations

from .risk import RiskTier, requires_approval


def should_auto_execute(tier: RiskTier) -> bool:
    return not requires_approval(tier)


def validate_typed_confirmation(expected: str, provided: str | None) -> bool:
    if expected is None:
        return True
    return (provided or '').strip() == expected.strip()
