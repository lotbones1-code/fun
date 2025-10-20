from dataclasses import dataclass

@dataclass
class RangeInputs:
    midpoint: float
    atr_4h: float
    regime_broken: bool = False
    skew_sign: int = 0

def compute_range(inp: RangeInputs):
    base = 1.0 * inp.atr_4h
    if inp.regime_broken:
        base = max(1.5 * inp.atr_4h, 2.0 * inp.atr_4h)
    lower = inp.midpoint - base
    upper = inp.midpoint + base
    skew = 0.3 * inp.atr_4h * inp.skew_sign
    return (lower - skew, upper - skew), base
