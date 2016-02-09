from simulator.BaseEvaluator import BaseEvaluator
from utils.csvdata import get_data_of_symbol
from analysis.indicators import kdj, bollinger_bands, adx
from analysis.candlestick_pattern import fractals


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
    Bull Percent: 48.5041175857%(143895) Bear Percent: 50.9751889703%(136794)
    """

    def __init__(self, start_date, end_date, symbols=None, target_period=5):
        ReverseEvaluator.__init__(self, start_date, end_date, symbols=symbols, target_period=target_period)


    def count_signals(self, prices, gain, result):
        kdj_val = kdj(prices)
        j_val = kdj_val['J']

        for i in range(1, len(gain) - self.target_period):
            if j_val[i - 1] < 0 and j_val[i] > 0:
                self.increase_bull_signal(result, gain[i] > 0)
            elif j_val[i - 1] > 100 and j_val[i] < 100:
                self.increase_bear_signal(result, gain[i] < 0)

        self.ts_print(result)


class BBReverseEvaluator(ReverseEvaluator):
    """
    Mode 1
    Bull Percent: 44.6552484393% (172356) Bear Percent: 48.1805518782% (173734)

    Mode 2
    Bull Percent: 50.9387985069% (70995) Bear Percent: 50.9602986088% (58940)
    """

    def __init__(self, start_date, end_date, symbols=None, target_period=3, mode=1):
        """
        Parameters
        -----------
        mode: int
            In different mode, the evaluator use different reverse signals.
            1: intersect middle band
            2: intersect lower band or upper band
        """
        ReverseEvaluator.__init__(self, start_date, end_date, symbols=symbols, target_period=target_period)
        self.mode = mode


    def count_signals(self, prices, gain, result):
        close = prices['Close']
        rm, upper_band, lower_band = bollinger_bands(close)

        if self.mode == 1:
            self.__mode_1(close, rm, gain, result)
        else:
            self.__mode_2(close, upper_band, lower_band, gain, result)

        self.ts_print(result)


    def __mode_1(self, close, rm, gain, result):
        for i in range(1, len(gain) - self.target_period):
            if close[i - 1] < rm[i - 1] and close[i] > rm[i]:
                self.increase_bull_signal(result, gain[i] > 0)
            elif close[i - 1] > rm[i - 1] and close[i] < rm[i]:
                self.increase_bear_signal(result, gain[i] < 0)


    def __mode_2(self, close, upper_band, lower_band, gain, result):
        for i in range(1, len(gain) - self.target_period):
            if close[i - 1] < lower_band[i - 1] and close[i] > lower_band[i]:
                self.increase_bull_signal(result, gain[i] > 0)
            elif close[i - 1] > upper_band[i - 1] and close[i] < upper_band[i]:
                self.increase_bear_signal(result, gain[i] < 0)


class ADXFRACReverseEvaluator(ReverseEvaluator):
    """
    """
    def __init__(self, start_date, end_date, symbols=None, target_period=3):
        ReverseEvaluator.__init__(self, start_date, end_date, symbols=symbols, target_period=target_period)


    def count_signals(self, prices, gain, result):
        frac, breakout = fractals(prices)
        adx_val, pdi, mdi = adx(prices)

        for i in range(5, len(gain) - self.target_period):
            if adx_val[i] > 20 and adx_val[i] > adx_val[i-1] and pdi[i] > mdi[i] and breakout[i] == 1:
                self.increase_bull_signal(result, gain[i] > 0)
            elif adx_val[i] > 20  and adx_val[i] > adx_val[i-1] and pdi[i] < mdi[i] and breakout[i] == -1:
                self.increase_bear_signal(result, gain[i] < 0)

        self.ts_print(result)