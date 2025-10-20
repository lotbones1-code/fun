def adjust_by_btc_coupling(prob_bull: float, corr_30d: float, btc_below_pivot_and_ma: bool, atr_widen: float):
    if corr_30d >= 0.6 and btc_below_pivot_and_ma:
        return max(0.0, prob_bull * 0.8), atr_widen + 0.5
    return prob_bull, atr_widen
