from simulator.BaseEvaluator import BaseEvaluator
from utils.csvdata import get_data_of_symbol
from analysis.indicators import kdj


class ReverseEvaluator(BaseEvaluator):

    def __init__(self, start_date, end_date, symbols=None, target_period=5):
        BaseEvaluator.__init__(self, start_date, end_date, symbols=symbols)
        self.target_period = target_period


    def real_evaluate(self, symbol):
        """
        This method does the real evaluation job. It must be thread safe.
        """
        prices = get_data_of_symbol(symbol, self.start_date, self.end_date, fill_empty=False)
        result = {"bull_signal_count": 0, "valid_bull_signal_count": 0,
                  "bear_signal_count": 0, "valid_bear_signal_count": 0,
                  "symbol": symbol}
        close = prices['Close']
        gain = close.shift(-self.target_period)/close - 1
        self.count_signals(prices, gain, result)
        return result


    def count_signals(self, prices, gain, result):
        raise NotImplementedError


    def generate_report(self):
        bull_signal_count = 0
        valid_bull_signal_count = 0
        bear_signal_count = 0
        valid_bear_signal_count = 0

        for result in self.results:
            bull_signal_count += result["bull_signal_count"]
            valid_bull_signal_count += result["valid_bull_signal_count"]
            bear_signal_count += result["bear_signal_count"]
            valid_bear_signal_count += result["valid_bear_signal_count"]

        self.report = "Bull Percent: {}({}) Bear Percent: {}({})"\
            .format(
                valid_bull_signal_count * 100.0 / bull_signal_count, bull_signal_count,
                valid_bear_signal_count * 100.0 / bear_signal_count, bear_signal_count
            )


class KDJReverseEvaluator(ReverseEvaluator):


    def __init__(self, start_date, end_date, symbols=None, target_period=5):
        ReverseEvaluator.__init__(self, start_date, end_date, symbols=symbols)


    def count_signals(self, prices, gain, result):
        kdj_val = kdj(prices)
        j_val = kdj_val['J']

        for i in range(1, len(gain) - self.target_period):
            if j_val[i - 1] < 0 and j_val[i] > 0:
                result["bull_signal_count"] += 1
                if gain[i] > 0:
                    result["valid_bull_signal_count"] += 1
            elif j_val[i - 1] > 100 and j_val[i] < 100:
                result["bear_signal_count"] += 1
                if gain[i] < 0:
                    result["valid_bear_signal_count"] += 1

        self.thread_lock.acquire()
        print result
        self.thread_lock.release()