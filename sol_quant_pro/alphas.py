import pandas as pd
import numpy as np

# Basic alphas used by the policy/AI layer

def alpha_trend(df):
    sig = np.where(df['ema_fast'] > df['ema_slow'], 1, -1)
    return pd.Series(sig, index=df.index, name='alpha_trend')

def alpha_meanrev(df):
    sig = np.where(df['bb_pos'] < 0.15, 1, np.where(df['bb_pos'] > 0.85, -1, 0))
    return pd.Series(sig, index=df.index, name='alpha_meanrev')

def alpha_breakout(df):
    win = 48  # ~4h breakout on 5m bars
    hi = df['high'].rolling(win).max()
    lo = df['low'].rolling(win).min()
    sig = np.where(df['close'] > hi.shift(1), 1, np.where(df['close'] < lo.shift(1), -1, 0))
    return pd.Series(sig, index=df.index, name='alpha_breakout')

def stack_alphas(df):
    A = pd.concat([alpha_trend(df), alpha_meanrev(df), alpha_breakout(df)], axis=1).fillna(0)
    A['alpha_ensemble'] = A.mean(axis=1)
    return A
