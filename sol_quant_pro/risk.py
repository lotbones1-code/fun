def position_size(account_equity: float, risk_per_trade: float, entry: float, stop: float):
    risk_amt = account_equity * risk_per_trade
    per_unit = abs(entry - stop)
    if per_unit <= 0: return 0.0
    return max(0.0, risk_amt / per_unit)
