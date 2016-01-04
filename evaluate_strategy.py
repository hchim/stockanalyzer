from strategy.BBStrategy import BBStrategy
from strategy.CMFStrategy import CMFStrategy
from strategy.StrategyEvaluator import StrategyEvaluator
from strategy.SMA13Strategy import SMA13Strategy

PERIOD1 = {"startdate": "2015-01-01", "enddate":"2015-12-30"}

SYMBOLS_IT = {
    "AAPL" : PERIOD1,
    "AMZN" : PERIOD1,
    "IBM" : PERIOD1,
    "BABA" : PERIOD1,
    "JMEI" : PERIOD1,
    "AMBA" : PERIOD1,
    "GOOG" : PERIOD1,
    "JD" : PERIOD1,
    "BIDU" : PERIOD1,
    "MSFT" : PERIOD1,
}

def evaluate_BB():
    strategy = BBStrategy()
    evaluator = StrategyEvaluator(strategy)
    evaluator.evaluate(SYMBOLS_IT)


def evaluate_CMF():
    strategy = CMFStrategy()
    evaluator = StrategyEvaluator(strategy)
    evaluator.evaluate(SYMBOLS_IT)


def evaluate_SMA13():
    strategy = SMA13Strategy()
    evaluator = StrategyEvaluator(strategy, allow_short=False)
    evaluator.evaluate(SYMBOLS_IT)


def evaluate_symbol(strategy, symbol, startdate, enddate):
    evaluator = StrategyEvaluator(strategy)
    evaluator.evaluate({symbol: {"startdate":startdate, "enddate": enddate}})
    evaluator.plot_order_signals(symbol)


if __name__ == "__main__":
    # evaluate_BB()
    # evaluate_CMF()
    evaluate_SMA13()
    # evaluate_symbol(SMA13Strategy(), "GOOG", "2015-01-01", "2015-12-31")