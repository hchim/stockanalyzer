from simulator.BaseEvaluator import BaseEvaluator
from utils.csvdata import get_data_of_symbol
from analysis.indicators import kdj, macd


class ReverseEvaluator(BaseEvaluator):
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

        self.report = "Bull Percent: {}% ({}) Bear Percent: {}% ({})"\
            .format(
                valid_bull_signal_count * 100.0 / bull_signal_count, bull_signal_count,
                valid_bear_signal_count * 100.0 / bear_signal_count, bear_signal_count
            )


    def increase_bull_signal(self, result, valid):
        result["bull_signal_count"] += 1
        if valid:
            result["valid_bull_signal_count"] += 1


    def increase_bear_signal(self, result, valid):
        result["bear_signal_count"] += 1
        if valid:
            result["valid_bear_signal_count"] += 1


class KDJReverseEvaluator(ReverseEvaluator):
    """
    mode 1:
    Bull Percent: 55.7251908397% (131) Bear Percent: 53.4482758621% (116)
    mode 2: k value [20, 80]
    Bull Percent: 76.9230769231% (13) Bear Percent: 41.1764705882% (17)
    """

    def __init__(self, start_date, end_date, symbols=None, thread_number=None, target_period=5, mode=1):
        """
        mode:  1: overbought and oversell signals. 2: cross signal
        """
        ReverseEvaluator.__init__(self, start_date, end_date, symbols=symbols,
                                  thread_number=thread_number, target_period=target_period)
        self.mode = mode


    def count_signals(self, prices, gain, result):
        kdj_val = kdj(prices)
        macd_val, signal, histgram = macd(prices)
        j_val = kdj_val['J']

        if self.mode == 1:
            self.__mode_1(j_val, macd_val, signal, gain, result)
        else:
            self.__mode_2(kdj_val["K"], kdj_val["J"], macd_val, signal, gain, result)

        self.ts_print(result)


    def __mode_1(self, j_val, macd_val, macd_signal, gain, result):
        for i in range(1, len(gain) - self.target_period):
            if j_val[i - 1] < 0 and j_val[i] > 0 and macd_val[i] > 0 and macd_signal[i] > macd_val[i]:
                self.increase_bull_signal(result, gain[i] > 0)
            elif j_val[i - 1] > 100 and j_val[i] < 100 and macd_val[i] < 0 and macd_signal[i] < macd_val[i]:
                self.increase_bear_signal(result, gain[i] < 0)


    def __mode_2(self, k_val, d_val, macd_val, macd_signal, gain, result):
        for i in range(1, len(gain) - self.target_period):
            if k_val[i - 1] < d_val[i - 1] and k_val[i] >= d_val[i] and k_val[i] < 20 and macd_val[i] > 0 and macd_signal[i] > macd_val[i]:
                self.increase_bull_signal(result, gain[i] > 0)
            elif k_val[i - 1] > d_val[i - 1] and k_val[i] <= d_val[i] and k_val[i] > 80 and macd_val[i] < 0 and macd_signal[i] < macd_val[i]:
                self.increase_bear_signal(result, gain[i] < 0)