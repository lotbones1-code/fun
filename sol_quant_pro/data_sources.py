
import time
import math
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
import ccxt

BINANCE_FAPI = 'https://fapi.binance.com'

def _usdm_symbol(symbol: str) => str:
    # 'SOL/USDT' -> 'SOLUSDT'
    return symbol.replace('/', '')

def fetch_binance_funding(symbol: str, timeout: float = 5.0) => Optional[float]:
    try:
        s = _usdm_symbol(symbol)
        url = f({BINANCE_FAPI})/fapi/v1/fundingRate"\n        r = requests.get(url, params={'symbol': s