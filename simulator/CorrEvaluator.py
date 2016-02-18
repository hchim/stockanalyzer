from simulator.BaseEvaluator import BaseEvaluator
from utils.csvdata import get_data_of_symbol
from analysis.basic import normalize

import numpy as np
import analysis.indicators as ind


class CorrEvaluator(BaseEvaluator):
    """
    This class evaluate the correlation of the symbol with the specified indicators.
    """

    def __init__(self, start_date, end_date, symbols=None, thread_number=None,
                 indicator={}, target="RETURN", target_period=5):
        """
        Parameters
        ----------
        indicators: dict
            the indicator to compare. for example:
            {"name": "obv", "column":"OBV", "normalize":True, "params": None}
            name: function name
            column: the column of the indicator value
            normalize: normalize the value
            params: parameters of the indicator
        target: String
            RETURN: find the correlation with the return after T days (T is the target period).
            PRICE: find the correlation with the price after T days.
        target_period: int
        """
        BaseEvaluator.__init__(self, start_date, end_date, symbols=symbols, thread_number=thread_number)
        self.indicator = indicator
        self.target = target
        self.target_period = target_period


    def real_evaluate(self, symbol):
        prices = get_data_of_symbol(symbol, self.start_date, self.end_date, fill_empty=False)
        result = {"symbol": symbol}
        target_values = self.__get_evaluate_target(prices)
        ind_vals = getattr(ind, self.indicator["name"])(prices, self.indicator["params"])
        ind_vals = ind_vals[self.indicator["column"]].dropna()
        if self.indicator["normalize"] and ind_vals[0] != 0:
            ind_vals = normalize(ind_vals)

        data = target_values.to_frame().join(ind_vals, how="inner")
        result["corr"] = data.corr(method="pearson").values[0,1]
        self.ts_print(result)

        return result


    def generate_report(self):
        corrs = np.zeros(len(self.results))
        for i in range(len(self.results)):
            corrs[i] = self.results[i]["corr"]

        self.report = "CORR: AVG:{} MIN:{} MAX:{} MEDIAN:{}".format(
            np.average(corrs), corrs.min(), corrs.max(), np.median(corrs)
        )


    def __get_evaluate_target(self, prices):
        values = None
        close = prices['Close']

        if self.target == "RETURN":
            values = close.shift(-1 * self.target_period)/close - 1
        elif self.target == "PRICE":
            values = normalize(close)
            values = values.shift(-1 * self.target_period)

        return values.dropna()