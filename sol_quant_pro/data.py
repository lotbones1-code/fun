import os, time
import pandas as pd
from datetime import datetime, timedelta, timezone
from broker import load_cfg, make_exchange

def ms_since(days: int) -> int:
    dt = datetime.now(timezone.utc) - timedelta(days=days)
    return int(dt.timestamp() * 1000)

def fetch_ohlcv():
    cfg = load_cfg()
    ex = make_exchange(cfg)
    sym = cfg['market']['symbol']
    tf = cfg['market']['timeframe']
    since = ms_since(cfg['market']['since_days'])
    limit = 1500
    all_rows = []
    ptr = since
    while True:
        batch = ex.fetch_ohlcv(sym, timeframe=tf, since=ptr, limit=limit)
        if not batch:
            break
        all_rows += batch
        ptr = batch[-1][0] + 1
        if len(batch) < limit:
            break
        time.sleep(ex.rateLimit/1000)
    df = pd.DataFrame(all_rows, columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    os.makedirs('data', exist_ok=True)
    out = 'data/' + sym.replace('/', '_') + '_' + tf + '.csv'
    df.to_csv(out, index=False)
    print('Wrote ' + out + ' rows=' + str(len(df)))
    return out

if __name__ == '__main__':
    fetch_ohlcv()
