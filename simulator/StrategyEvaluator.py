from simulator.BaseEvaluator import BaseEvaluator
from simulator.TradeSimulator import TradeSimulator
from utils.csvdata import get_data_of_symbol
from analysis.portfolio import get_portfolio_stats

import importlib
import numpy as np

class StrategyEvaluator(BaseEvaluator):

    def __init__(self, start_date, end_date, strategy_name, symbols=None, thread_number=None):
        BaseEvaluator.__init__(self, start_date, end_date, symbols=symbols, thread_number=thread_number)
        self.strategy_name = strategy_name


    def real_evaluate(self, symbol):
        prices = get_data_of_symbol(symbol, self.start_date, self.end_date, fill_empty=False)
        module = importlib.import_module("strategy.{}".format(self.strategy_name))
        strategy = getattr(module, self.strategy_name)()
        orders = strategy.generate_orders(prices, symbol)

        result = {"symbol": symbol}
        simulator = TradeSimulator()
        closes = prices['Close'].to_frame()
        closes.rename(columns={"Close":symbol}, inplace=True)
        port_vals = simulator.simulate(prices=closes, orders=orders)
        result["cum_ret"], result["avg_daily_ret"], result["std_daily_ret"], result["sharpe_ratio"] = \
            get_portfolio_stats(port_vals.iloc[:, 0])

        self.ts_print(result)
        return result


    def generate_report(self):
        cum_ret = np.zeros(len(self.results))
        sharpe_ratio = np.zeros(len(self.results))

        for i in range(len(self.results)):
            cum_ret[i] = self.results[i]["cum_ret"]
            sharpe_ratio[i] = self.results[i]["sharpe_ratio"]

        self.report = "Cumulative return: AVG:{} MIN:{} MAX:{} MEDIAN:{} \n " \
                      "Sharpe ratio: AVG:{} MIN:{} MAX:{} MEDIAN:{}" \
            .format(
            np.average(cum_ret), cum_ret.min(), cum_ret.max(), np.median(cum_ret),
            np.average(sharpe_ratio), sharpe_ratio.min(), sharpe_ratio.max(), np.median(sharpe_ratio)
        )