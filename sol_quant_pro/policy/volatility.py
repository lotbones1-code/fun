def volatility_discipline(bb_expanding: bool, atr_4h_ddelta_pct: float, base_half_range_atr: float) -> float:
    widen = 0.0
    if bb_expanding or atr_4h_ddelta_pct >= 0.20:
        widen += 0.25
    return base_half_range_atr * (1.0 + widen)
