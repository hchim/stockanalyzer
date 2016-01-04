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
        rsi = inds["RSI"]
        macd = inds["MACD_Val"]
        signal = inds["MACD_Signal"]

        return cmf > 0.05 and rsi < 70 and signal > macd


    def is_sell_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        cmf = inds["CMF"]
        pre_rsi = pre_inds["RSI"]
        rsi = inds["RSI"]
        macd = inds["MACD_Val"]
        signal = inds["MACD_Signal"]

        return cmf < -0.05 or (pre_rsi > 70 and rsi < 70) or signal < macd