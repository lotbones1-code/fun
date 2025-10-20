from dataclasses import dataclass

@dataclass
class BiasInputs:
    last_4h_close: float
    daily_pivot: float
    ma_4h_50: float

def bias_gate(inp: BiasInputs) -> str:
    if inp.last_4h_close > inp.daily_pivot and inp.last_4h_close > inp.ma_4h_50:
        return 'Bullish'
    if inp.last_4h_close < inp.daily_pivot and inp.last_4h_close < inp.ma_4h_50:
        return 'Bearish'
    return 'Neutral'
