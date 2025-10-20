import time
import pandas as pd
from broker import load_cfg, make_exchange, PaperBroker
from features import engineer_5m
from utils import resample_to_4h, ema, atr, pivot_levels_from_daily
from policy.bias_gate import BiasInputs, bias_gate
from policy.derivs_filter import DerivsInputs, derivatives_confirmation
from policy.range_engine import RangeInputs, compute_range
from policy.targets import point_target
from policy.guards import sanity_failsafe

from risk import position_size

def last_n(ex, symbol, timeframe, n):
    ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=n)
    df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    return df

def main():
    cfg = load_cfg()
    ex = make_exchange(cfg)
    sym = cfg['market']['symbol']; tf = cfg['market']['timeframe']
    fee = cfg['fees']['taker']
    pb = PaperBroker(fee=fee); pb.reset(cfg['risk']['account_equity'])

    while True:
        try:
            raw = last_n(ex, sym, tf, n=min(1000, cfg['live']['max_candles']))
            fe = engineer_5m(raw)
            h4 = resample_to_4h(raw)
            h4['ma50'] = ema(h4['close'], 50)
            h4['atr14'] = atr(h4['high'], h4['low'], h4['close'], 14)
            dly = raw.set_index('timestamp').resample('1D').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna().reset_index()
            piv = pivot_levels_from_daily(dly)
            last4 = h4.iloc[-1]
            gate = bias_gate(BiasInputs(float(last4['close']), float(piv['P']), float(last4['ma50'])))
            derivs = derivatives_confirmation(DerivsInputs(price=float(last4['close']), pivot=float(piv['P']), oi_24h_change=0.0, funding_rate=0.0))
            skew_sign = 1 if derivs == 'Neutral_TacticalBullish' else (-1 if derivs == 'Neutral_TacticalBearish' else 0)
            rng, base = compute_range(RangeInputs(midpoint=float(piv['P']), atr_4h=float(last4['atr14']), regime_broken=False, skew_sign=skew_sign))
            favored_half = 'upper' if skew_sign>0 else ('lower' if skew_sign<0 else 'none')
            tgt = point_target(float(piv['P']), favored_half if favored_half!='none' else 'upper', float(piv['P']), float(piv['R1']), float(piv['S1']))
            gate_adj, half_adj = sanity_failsafe(gate, favored_half if favored_half!='none' else 'upper')
            print(str(last4['timestamp']), 'gate=', gate, 'derivs=', derivs, 'range=', rng, 'target=', tgt, 'pos=', pb.pos, 'eq=', pb.equity)
        except Exception as e:
            print('Loop error:', repr(e))
        time.sleep(cfg['live']['poll_seconds'])

if __name__ == '__main__':
    main()
