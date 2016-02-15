from simulator.StrategyEvaluator import StrategyEvaluator

PERIOD = {"startdate": "2015-01-01", "enddate":"2015-12-30"}

SYMBOLS_IT = ['AAPL', 'AMZN', 'GOOG', 'FB', 'IBM', 'MSFT', 'QCOM', 'ORCL', 'NFLX',
              'INTL', 'SAP', 'CRM', 'VMW', 'PANW', 'CA', 'INTU', 'BABA', 'JD',
              'BIDU']

SYMBOLS_CN = ["JD","BIDU","BABA","JMEI","XNET","CMCM","VIPS","YOKU",
              "WUBA","SOHU","SINA","SFUN","BITA","CTRP","TOUR","WBAI",
              "CCIH","EHIC","KNDI"]


def evaluate_BB():
    evaluator = StrategyEvaluator(PERIOD["startdate"], PERIOD["enddate"], "BBStrategy", symbols=SYMBOLS_IT)
    evaluator.start()
    evaluator.dump_report()


def evaluate_CMF():
    evaluator = StrategyEvaluator(PERIOD["startdate"], PERIOD["enddate"], "CMFStrategy", symbols=SYMBOLS_IT, thread_number=1)
    evaluator.start()
    evaluator.dump_report()


def evaluate_SMA13():
    evaluator = StrategyEvaluator(PERIOD["startdate"], PERIOD["enddate"], "SMA13Strategy", symbols=SYMBOLS_IT)
    evaluator.start()
    evaluator.dump_report()


if __name__ == "__main__":
    # evaluate_BB()
    evaluate_CMF()
    # evaluate_SMA13()