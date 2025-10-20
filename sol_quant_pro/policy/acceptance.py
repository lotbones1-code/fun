from dataclasses import dataclass

@dataclass
class AcceptanceInputs:
    closes_15m_beyond: int
    close_1h_beyond: bool
    confirming_delta: bool

def accepted(inp: AcceptanceInputs) -> bool:
    return (inp.close_1h_beyond or inp.closes_15m_beyond >= 2) and inp.confirming_delta
