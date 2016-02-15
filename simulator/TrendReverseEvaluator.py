import analysis.indicator_feature as indfr

from simulator.BaseEvaluator import BaseEvaluator
from utils.csvdata import get_data_of_symbol

class TrendReverseEvaluator(BaseEvaluator):
    """
    This class count the number of bull/bear signals and count the number of
    valid bull/bear signals (price increasing or decreasing in the target
    period).
    """

    def __init__(self, start_date, end_date, symbols=None, thread_number=None, target_period=5):
        BaseEvaluator.__init__(self, start_date, end_date, symbols=symbols, thread_number=thread_number)
        self.target_period = target_period


    def real_evaluate(self, symbol):
        prices = get_data_of_symbol(symbol, self.start_date, self.end_date, fill_empty=False)
        result = {"bull_signal_count": 0, "valid_bull_signal_count": 0,
                  "bear_signal_count": 0, "valid_bear_signal_count": 0,
                  "symbol": symbol}
        close = prices['Close']
        gain = close.shift(-self.target_period)/close - 1
        self.count_signals(prices, gain, result)
        return result


    def count_signals(self, prices, gain, result):
        """
        Count the number of bull/bear signals.
        """
        raise NotImplementedError


    def generate_report(self):
        """
        Generate evaluation report.
        """
        bull_signal_count = 0
        valid_bull_signal_count = 0
        bear_signal_count = 0
        valid_bear_signal_count = 0

        for result in self.results:
            bull_signal_count += result["bull_signal_count"]
            valid_bull_signal_count += result["valid_bull_signal_count"]
            bear_signal_count += result["bear_signal_count"]
            valid_bear_signal_count += result["valid_bear_signal_count"]

        bull_percent = valid_bull_signal_count * 100.0 / bull_signal_count if bull_signal_count > 0 else 0
        bear_percent = valid_bear_signal_count * 100.0 / bear_signal_count if bear_signal_count > 0 else 0
        self.report = "Bull Percent: {}% ({}) Bear Percent: {}% ({})"\
            .format(
                bull_percent, bull_signal_count,
                bear_percent, bear_signal_count
            )


    def increase_bull_signal(self, result, valid):
        result["bull_signal_count"] += 1
        if valid:
            result["valid_bull_signal_count"] += 1


    def increase_bear_signal(self, result, valid):
        result["bear_signal_count"] += 1
        if valid:
            result["valid_bear_signal_count"] += 1


class CompositeTREvaluator(TrendReverseEvaluator):

    def __init__(self, start_date, end_date, features,
                 symbols=None, thread_number=None, target_period=5):
        """
        Parameters
        -----------
        features: list(tuple)
            tuple[0]: function name of the feature
            tuple[1]: parameters of the feature
        """
        TrendReverseEvaluator.__init__(self, start_date, end_date, symbols=symbols,
                                  thread_number=thread_number, target_period=target_period)
        self.features = features


    def count_signals(self, prices, gain, result):
        data = []
        for f in self.features:
            values = getattr(indfr, f[0])(prices, f[1])
            data.append(values)

        for i in range(1, len(gain) - self.target_period):
            if self.__check_signal(data, i, 1):
                self.increase_bull_signal(result, gain[i] > 0)
            elif self.__check_signal(data, i, -1):
                self.increase_bear_signal(result, gain[i] < 0)

        self.ts_print(result)


    def __check_signal(self, features, index, value):
        for feature in features:
            if feature[index] != value:
                return False

        return True