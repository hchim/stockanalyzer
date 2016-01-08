from strategy.Strategy import Strategy

"""

"""
class CMFStrategy(Strategy):


    def __init__(self):
        params = {"CMF":None, "RSI": {"window":14}, "MACD": None}
        super(CMFStrategy, self).__init__(params)


    def is_buy_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        cmf = inds["CMF"]
        pre_cmf = pre_inds["CMF"]
        rsi = inds["RSI"]
        macd = inds["MACD_Val"]
        pre_macd = pre_inds["MACD_Val"]
        signal = inds["MACD_Signal"]

        # cmf cross 0.05 AND rsi not overbought AND macd signal increase
        return pre_cmf < 0.05 and cmf > 0.05 and signal < macd and pre_macd < macd


    def is_sell_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        cmf = inds["CMF"]
        pre_rsi = pre_inds["RSI"]
        rsi = inds["RSI"]
        macd = inds["MACD_Val"]
        signal = inds["MACD_Signal"]

        return cmf < -0.05 or signal > macd