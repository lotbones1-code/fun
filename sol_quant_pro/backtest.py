import pandas as pd
import yaml
from alphas import stack_alphas
from features import engineer_5m
from utils import resample_to_4h, ema, atr, pivot_levels_from_daily
from policy.bias_gate import BiasInputs, bias_gate
from policy.derivs_filter import DerivsInputs, derivatives_confirmation
from policy.range_engine import RangeInputs, compute_range
from policy.acceptance import AcceptanceInputs, accepted
from policy.targets import point_target
from policy.guards import sanity_failsafe

from risk import position_size

# Minimal backtest that applies policy constraints and optional AI gating (to be added)

def load_cfg():
    with open('config.yaml','r') as f: return yaml.safe_load(f)

def load_data(cfg):
    sym = cfg['market']['symbol'].replace('/','_'); tf = cfg['market']['timeframe']
    return pd.read_csv(f'data/{sym}_{tf}.csv', parse_dates=['timestamp'])

def backtest():
    cfg = load_cfg()
    raw = load_data(cfg)
    fe = engineer_5m(raw)
    # Build 4H frame for policy inputs
    h4 = resample_to_4h(raw)
    h4['ma50'] = ema(h4['close'], 50)
    h4['atr14'] = atr(h4['high'], h4['low'], h4['close'], 14)

    # Daily pivots from 4H aggregated to daily
    dly = raw.set_index('timestamp').resample('1D').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna().reset_index()
    piv = pivot_levels_from_daily(dly)

    last4 = h4.iloc[-1]
    gate = bias_gate(BiasInputs(last4['close'], piv['P'], last4['ma50']))

    # Derivs filter placeholders (user to wire real feeds)
    derivs = derivatives_confirmation(DerivsInputs(price=float(last4['close']), pivot=float(piv['P']), oi_24h_change=0.0, funding_rate=0.0))
    skew_sign = 1 if derivs == 'Neutral_TacticalBullish' else (-1 if derivs == 'Neutral_TacticalBearish' else 0)

    rng, base = compute_range(RangeInputs(midpoint=piv['P'], atr_4h=float(last4['atr14']), regime_broken=False, skew_sign=skew_sign))

    favored_half = 'upper' if skew_sign>0 else ('lower' if skew_sign<0 else 'none')
    tgt = point_target(piv['P'], favored_half if favored_half!='none' else 'upper', piv['P'], piv['R1'], piv['S1'])
    gate_adj, half_adj = sanity_failsafe(gate, favored_half if favored_half!='none' else 'upper')

    print('Bias Gate:', gate, 'Derivs:', derivs)
    print('Range:', rng, 'Target:', tgt, 'GateAdj:', gate_adj, 'HalfAdj:', half_adj)

if __name__ == '__main__':
    backtest()
