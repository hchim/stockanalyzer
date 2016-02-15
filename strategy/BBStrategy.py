from strategy.Strategy import Strategy

"""
A basic Bollinger Band trading strategy works as follows: There are two potential entries, long and short.
The long entry is made when the price transitions from below the lower band to above the lower band. This
indicates that the stock price has moved substantially away from the moving average, but is now moving back
towards the moving average. When this entry signal criteria is met, buy the stock and hold it until the exit.
The exit signal occurs when the price moves from below the SMA to above it.

The short entry and exit are mirrors of the long entry and exit: The short entry is made when the price
transitions from above the upper band to below the upper band. This indicates that the stock price has
moved substantially away from the moving average, but is now moving back towards the moving average.
When this entry signal criteria is met, short the stock and hold it until the exit. The exit signal
occurs when the price moves from above the SMA to below it.
"""
class BBStrategy(Strategy):


    def __init__(self):
        params = {"BB":{"window": 20}}
        super(BBStrategy, self).__init__(params)


    def is_buy_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        return pre_prices["Close"] < inds["Lower"] and prices["Close"] > inds["Lower"]


    def is_sell_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        return pre_prices["Close"] < inds["Middle"] and prices["Close"] > inds["Middle"]


    def is_short_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        return pre_prices["Close"] > inds["Upper"] and prices["Close"] < inds["Upper"]


    def is_cover_signal(self, inds, pre_inds, prices, pre_prices):
        if pre_prices is None or pre_inds is None:
            return False
        return pre_prices["Close"] > inds["Middle"] and prices["Close"] < inds["Middle"]