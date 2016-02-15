from strategy.Strategy import Strategy


class CMFStrategy(Strategy):


    def __init__(self):
        params = {"CMF":{"window": 20},
                  "RSI": {"window":14}, "MACD": {"windows": [12, 26, 9]}}
        super(CMFStrategy, self).__init__(params)


    def is_buy_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        cmf = inds["CMF"]
        pre_cmf = pre_inds["CMF"]
        macd = inds["DIFF"]
        pre_macd = pre_inds["DIFF"]
        signal = inds["DEA"]

        # cmf cross 0.05 AND rsi not overbought AND macd signal increase
        return pre_cmf < 0.05 and cmf > 0.05 and signal < macd and pre_macd < macd


    def is_sell_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        cmf = inds["CMF"]
        macd = inds["DIFF"]
        signal = inds["DEA"]

        return cmf < -0.05 or signal > macd