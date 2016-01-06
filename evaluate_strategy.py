from strategy.BBStrategy import BBStrategy
from strategy.CMFStrategy import CMFStrategy
from strategy.StrategyEvaluator import StrategyEvaluator
from strategy.SMA13Strategy import SMA13Strategy

PERIOD1 = {"startdate": "2015-01-01", "enddate":"2015-12-30"}

SYMBOLS_IT = {
    "AAPL" : PERIOD1,
    "AMZN" : PERIOD1,
    "IBM" : PERIOD1,
    "AMBA" : PERIOD1,
    "GOOG" : PERIOD1,
    "MSFT" : PERIOD1,
}

SYMBOLS_CN = {
    "JD" : PERIOD1,
    "BIDU" : PERIOD1,
    "BABA" : PERIOD1,
    "JMEI" : PERIOD1,
    "XNET" : PERIOD1,
    "CMCM" : PERIOD1,
    "VIPS" : PERIOD1,
    "YOKU" : PERIOD1,
    # "NETS" : PERIOD1,
    "WUBA" : PERIOD1,
    "SOHU" : PERIOD1,
    "SINA" : PERIOD1,
    "SFUN" : PERIOD1,
    "BITA" : PERIOD1,
    "CTRP" : PERIOD1,
    # "QUNR" : PERIOD1,
    "TOUR" : PERIOD1,
    "WBAI" : PERIOD1,
    "CCIH" : PERIOD1,
    "EHIC" : PERIOD1,
    "KNDI" : PERIOD1,
}

def evaluate_BB():
    strategy = BBStrategy()
    evaluator = StrategyEvaluator(strategy)
    evaluator.evaluate(SYMBOLS_IT)


def evaluate_CMF():
    strategy = CMFStrategy()
    evaluator = StrategyEvaluator(strategy)
    evaluator.evaluate(SYMBOLS_CN)


def evaluate_SMA13():
    strategy = SMA13Strategy()
    evaluator = StrategyEvaluator(strategy, allow_short=False)
    evaluator.evaluate(SYMBOLS_CN)


def evaluate_symbol(strategy, symbol, startdate, enddate):
    evaluator = StrategyEvaluator(strategy)
    evaluator.evaluate({symbol: {"startdate":startdate, "enddate": enddate}})
    evaluator.plot_order_signals(symbol)


if __name__ == "__main__":
    # evaluate_BB()
    # evaluate_CMF()
    # evaluate_SMA13()
    evaluate_symbol(CMFStrategy(), "WBAI", "2015-01-25", "2015-09-30")