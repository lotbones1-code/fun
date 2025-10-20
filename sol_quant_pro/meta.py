import pandas as pd
import numpy as np
import yaml, joblib, os
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor

FEATS = ['ret1','ret5','ret20','roll_std_20','roll_std_100','ema_diff','macd','macd_sig','macd_diff','rsi','stoch_k','stoch_d','bb_pos','atr_norm','hl_range','close_pos']

def load_cfg():
    with open('config.yaml','r') as f: return yaml.safe_load(f)

def train():
    cfg = load_cfg()
    df = pd.read_csv('data/features.csv', parse_dates=['timestamp'])
    X = df[FEATS].values
    y_cls = df['label_up'].values
    y_reg = df['fwd_ret'].values

    if cfg['strategy']['ai_model'] == 'xgboost':
        cls = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0, n_jobs=-1, tree_method='hist')
        reg = XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0, n_jobs=-1, tree_method='hist')
    else:
        cls = RandomForestClassifier(n_estimators=400, max_depth=6, n_jobs=-1)
        reg = RandomForestRegressor(n_estimators=400, max_depth=6, n_jobs=-1)

    cls_pipe = Pipeline([('scaler', StandardScaler()), ('model', cls)])
    reg_pipe = Pipeline([('scaler', StandardScaler()), ('model', reg)])

    cls_pipe.fit(X, y_cls)
    reg_pipe.fit(X, y_reg)

    os.makedirs('artifacts', exist_ok=True)
    joblib.dump({'pipe': cls_pipe, 'feats': FEATS}, 'artifacts/cls.joblib')
    joblib.dump({'pipe': reg_pipe, 'feats': FEATS}, 'artifacts/reg.joblib')
    print('Wrote artifacts/cls.joblib and artifacts/reg.joblib')

if __name__ == '__main__':
    train()
