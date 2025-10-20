import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange, BollingerBands

# Core feature engineering for 5m data.
# Expects columns: timestamp, open, high, low, close, volume (timestamp tz-aware UTC).

def engineer_5m(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['ret1'] = df['close'].pct_change()
    df['ret5'] = df['close'].pct_change(5)
    df['ret20'] = df['close'].pct_change(20)

    df['roll_std_20'] = df['ret1'].rolling(20).std()
    df['roll_std_100'] = df['ret1'].rolling(100).std()

    ema50 = EMAIndicator(close=df['close'], window=50).ema_indicator()
    ema200 = EMAIndicator(close=df['close'], window=200).ema_indicator()
    df['ema_fast'] = ema50
    df['ema_slow'] = ema200
    df['ema_diff'] = (ema50 - ema200) / df['close']

    macd = MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_sig'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    rsi = RSIIndicator(close=df['close'], window=14).rsi()
    df['rsi'] = rsi

    stoch = StochasticOscillator(high=df['high'], low=df['low'], close=df['close'])
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()

    bb = BollingerBands(close=df['close'], window=20, window_dev=2.0)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    df['bb_pos'] = (df['close'] - df['bb_low']) / (df['bb_high'] - df['bb_low'] + 1e-9)

    atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
    df['atr'] = atr
    df['atr_norm'] = atr / df['close']

    df['hl_range'] = (df['high'] - df['low']) / df['close']
    df['close_pos'] = (df['close'] - df['low']) / (df['high'] - df['low'] + 1e-9)
    return df

# Utility to compute previous UTC day H/L/C and classic pivots.

def prior_day_pivots(df_d: pd.DataFrame):
    # Expects daily candles with columns high, low, close and timestamp.
    last = df_d.iloc[-1]
    H, L, C = float(last['high']), float(last['low']), float(last['close'])
    P = (H + L + C) / 3.0
    S1 = 2*P - H
    R1 = 2*P - L
    return {'H': H, 'L': L, 'C': C, 'P': P, 'S1': S1, 'R1': R1}
