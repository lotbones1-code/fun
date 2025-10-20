import os
import ccxt
import yaml

def load_cfg(path: str = "config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def make_exchange(cfg):
    name = cfg["exchange"]["name"].lower()
    testnet = cfg["exchange"]["testnet"]
    key = os.getenv("BINANCE_API_KEY","")
    sec = os.getenv("BINANCE_SECRET","")
    if name == "binance":
        ex = ccxt.binanceusdm({"apiKey": key, "secret": sec, "enableRateLimit": True})
        ex.set_sandbox_mode(testnet)
        return ex
    raise ValueError(f"Unsupported exchange: {name}")

class PaperBroker:
    def __init__(self, fee=0.0006):
        self.equity = None
        self.pos = 0
        self.entry = 0.0
        self.qty = 0.0
        self.fee = fee

    def reset(self, equity):
        self.equity = equity
        self.pos = 0
        self.entry = 0.0
        self.qty = 0.0

    def enter(self, side, price, qty):
        self.pos = 1 if side.upper()=="LONG" else -1
        self.entry = price
        self.qty = qty

    def exit(self, price):
        if self.pos == 0: return 0.0
        pnl = (price - self.entry) * self.qty * self.pos
        fees = self.fee * abs(self.qty) * (self.entry + price)
        self.equity += pnl - fees
        self.pos = 0
        self.entry = 0.0
        self.qty = 0.0
        return pnl - fees
