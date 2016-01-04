from strategy.Strategy import Strategy

"""

"""
class SMA13Strategy(Strategy):


    def __init__(self):
        params = {"SMA5":None, "SMA13": None, "SMA60": None}
        super(SMA13Strategy, self).__init__(params)


    def is_buy_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        sma5 = inds["SMA5"]
        sma13 = inds["SMA13"]
        sma60 = inds["SMA60"]
        close = prices["Close"]
        return sma5 > sma13 and close > sma5 and sma13 > sma60


    def is_sell_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        sma5 = inds["SMA5"]
        sma13 = inds["SMA13"]
        close = prices["Close"]

        return close < sma5 or sma5 < sma13