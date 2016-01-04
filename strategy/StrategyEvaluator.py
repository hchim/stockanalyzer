from utils.webdata import get_data_of_symbol
from simulator.TradeSimulator import TradeSimulator
from analysis.portfolio import get_portfolio_stats
from utils.draw import plot_single_symbol

import numpy as np


class StrategyEvaluator(object):

    def __init__(self, strategy, allow_short=True, start_value=1000000):
        self.strategy = strategy
        self.allow_short = allow_short
        self.start_value = start_value
        self.simulator = TradeSimulator(allow_short=self.allow_short, start_val=self.start_value)


    def evaluate(self, symbols):
        self.symbols = symbols

        cumulative_ret = []
        sharp_ratio = []
        for symbol in symbols.keys():
            params = symbols[symbol]
            startdate = params["startdate"]
            enddate = params["enddate"]
            ret, sr = self.evaluate_symbol(symbol, startdate, enddate)
            cumulative_ret.append(ret)
            sharp_ratio.append(sr)

            print symbol
            print "Return: ", ret
            print "Sharp Ratio: ", sr

        print
        print "min return: ", np.min(cumulative_ret)
        print "average return: ", np.mean(cumulative_ret)
        print "average sharp ratio: ", np.mean(sharp_ratio)


    def evaluate_symbol(self, symbol, startdate, enddate):
        if self.symbols is None:
            return

        prices = get_data_of_symbol(symbol, startdate, enddate, fill_empty=False)
        orders = self.strategy.generate_orders(prices, symbol,
            allow_short=self.allow_short, start_value=self.start_value)
        self.symbols[symbol]["prices"] = prices
        self.symbols[symbol]["orders"] = orders

        closes = prices.loc[:, 'Close'].to_frame()
        closes.rename(columns={"Close":symbol}, inplace=True)

        port_vals = self.simulator.simulate(prices=closes, orders=orders)
        self.symbols[symbol]["port_vals"] = port_vals
        cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_vals.iloc[:, 0])
        return cum_ret, sharpe_ratio


    def plot_order_signals(self, symbol):
        if self.symbols is None:
            return

        plot_single_symbol(self.symbols[symbol]["prices"],
                           indicators=self.strategy.get_indicator_params(),
                           orders=self.symbols[symbol]["orders"])
