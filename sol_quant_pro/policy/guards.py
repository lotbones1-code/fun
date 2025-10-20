def sanity_failsafe(bias_gate_result: str, computed_target_half: str):
    if bias_gate_result == 'Bullish' and computed_target_half == 'lower':
        return 'Neutral', 'upper'
    if bias_gate_result == 'Bearish' and computed_target_half == 'upper':
        return 'Neutral', 'lower'
    return bias_gate_result, computed_target_half

def post_print_guard(exited_by_half_atr: bool, band_edges, atr):
    if exited_by_half_atr:
        lower, upper = band_edges
        return (lower - 0.5*atr, upper + 0.5*atr)
    return band_edges
