from dataclasses import dataclass

@dataclass
class DerivsInputs:
    price: float
    pivot: float
    oi_24h_change: float
    funding_rate: float

def derivatives_confirmation(inp: DerivsInputs) -> str:
    if inp.price < inp.pivot and inp.oi_24h_change <= 0 and inp.funding_rate >= 0:
        return 'Neutral_TacticalBearish'
    if inp.price > inp.pivot and inp.oi_24h_change >= 0 and inp.funding_rate <= 0:
        return 'Neutral_TacticalBullish'
    return 'None'
