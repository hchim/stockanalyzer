from simulator.TrendReverseEvaluator import CompositeTREvaluator


IT_SYMBOLS = ['AAPL', 'AMZN', 'GOOG', 'FB', 'IBM', 'MSFT', 'QCOM', 'ORCL', 'NFLX',
              'INTL', 'SAP', 'CRM', 'VMW', 'PANW', 'CA', 'INTU', 'BABA', 'JD',
              'BIDU']

def test_trevaluator():
    """
    SMA_CROSS [5, 10]: Bull Percent: 54.0909090909% (220) Bear Percent: 44.6428571429% (224)
    EMA_CROSS [5, 10]: Bull Percent: 53.050397878% (377) Bear Percent: 44.9612403101% (387)
    KDJ_OVER [1, 100]: Bull Percent: 52.8150134048% (373) Bear Percent: 49.3917274939% (411)
    KDJ_CROSS [30, 70]: Bull Percent: 52.1739130435% (368) Bear Percent: 48.6899563319% (458)
    TREND_SMA and KDJ_OVER: Bull Percent: 71.4285714286% (7) Bear Percent: 41.6666666667% (12)
    CCI_OVER[window=10]: Bull Percent: 62.8787878788% (132) Bear Percent: 46.2809917355% (121)
    """
    featrues = [
        # ("trend_macd_zero_line", None),
        ("reverse_cci_over_sell_buy", {"window": 10})
    ]
    evaluator = CompositeTREvaluator('2014-01-01', '2016-02-01',
                                     features=featrues, symbols=IT_SYMBOLS)
    evaluator.start()
    evaluator.dump_report()


if __name__ == "__main__":
    test_trevaluator()