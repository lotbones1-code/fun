def point_target(midpoint: float, favored_half: str, pivot: float, r1: float, s1: float) -> float:
    if favored_half == 'upper':
        tgt = (pivot + r1) / 2.0
    elif favored_half == 'lower':
        tgt = (s1 + pivot) / 2.0
    else:
        tgt = pivot
    return round(tgt, 2)
