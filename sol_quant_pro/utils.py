import pandas as pd
import numpy as np

def resample_to_4h(df5: pd.DataFrame) -> pd.DataFrame:
    # 5m -> 4H OHLCV
    df = df5.set_index('timestamp').sort_index()
    o = df['open'].resample('4H').first()
    h = df['high'].resample('4H').max()
    l = df['low'].resample('4H').min()
    c = df['close'].resample('4H').last()
    v = df['volume'].resample('4H').sum()
    out = pd.DataFrame({'open':o,'high':h,'low':l,'close':c,'volume':v})
    out = out.dropna().reset_index()
    return out

def ema(series: pd.Series, n: int) -> pd.Series:
    return series.ewm(span=n, adjust=False).mean()

def atr(high: pd.Series, low: pd.Series, close: pd.Series, n: int=14) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat([(high-low), (high-prev_close).abs(), (low-prev_close).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()

def pivot_levels_from_daily(df_daily: pd.DataFrame):
    last = df_daily.iloc[-1]
    H,L,C = float(last['high']), float(last['low']), float(last['close'])
    P=(H+L+C)/3.0; S1=2*P-H; R1=2*P-L
    return {'H':H,'L':L,'C':C,'P':P,'S1':S1,'R1':R1}

