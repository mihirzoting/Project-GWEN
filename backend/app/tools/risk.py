from enum import Enum


class RiskTier(str, Enum):
    T1 = 'T1'
    T2 = 'T2'
    T3 = 'T3'
    T4 = 'T4'


def requires_approval(tier: RiskTier) -> bool:
    return tier in {RiskTier.T2, RiskTier.T3, RiskTier.T4}


def confirmation_type(tier: RiskTier) -> str | None:
    if tier == RiskTier.T2:
        return 'confirm'
    if tier == RiskTier.T3:
        return 'blocking'
    if tier == RiskTier.T4:
        return 'typed'
    return None
