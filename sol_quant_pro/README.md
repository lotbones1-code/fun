# SOL Quant Pro — Hybrid (Rule‑Based + AI) Starter

A modular, production‑oriented Solana (SOL/USDT) quant framework that supports:
- Rule‑based alphas (trend, mean‑reversion, breakout).
- AI meta‑model (scikit‑learn/XGBoost) to ensemble alphas and features.
- Walk‑forward training and evaluation.
- Vectorized backtester with costs, ATR sizing, and drawdown guard.
- Paper‑trading loop via ccxt; Binance futures testnet ready.

Use this to iterate quickly. Ship signals first (Discord/Telegram), then graduate to small live sizing.

## Quickstart
1) Python 3.10+ recommended.
2) Install deps:
```
pip install -r requirements.txt
```
3) Configure in `config.yaml`. Keep `live.trading: false` while testing.
4) Fetch data:
```
python data.py
```
5) Build features + train AI (optional):
```
python features.py
python meta.py
```
6) Backtest:
```
python backtest.py
```
7) Paper‑trade loop (simulated fills):
```
python live.py
```

## Notes
- Default symbol: SOL/USDT (Binance USDM), timeframe: 5m, lookback: 30 days.
- Targets: classification on forward return sign and regression on next‑k return; strategy uses thresholds.
- AI improves when: (a) enough data; (b) walk‑forward splits; (c) regular re‑training.
- Never deploy live without months of out‑of‑sample. Start tiny.
