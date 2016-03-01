from simulator.StrategyEvaluator import StrategyEvaluator
from strategy.KDJStrategy import KDJStrategy
from utils.csvdata import get_data_of_symbol
from gui.SymbolPlotter import SymbolPlotter

IT_SYMBOLS = ['AAPL', 'AMZN', 'GOOG', 'FB', 'IBM', 'MSFT', 'QCOM', 'ORCL', 'NFLX',
              'INTL', 'SAP', 'CRM', 'VMW', 'PANW', 'CA', 'INTU', 'BABA', 'JD',
              'BIDU']


def test_kdjstrategy(symbol):
    strategy = KDJStrategy()
    prices = get_data_of_symbol(symbol, '2014-01-01', '2016-02-01')
    orders = strategy.generate_orders(prices, symbol)

    plotter = SymbolPlotter(max_candles=150)
    plotter.plot_single_symbol(prices, indicators={"stoch": {"windows": [14, 3, 3]}}, orders=orders)
    print orders


def evaluate_kdjstrategy():
    evaluator = StrategyEvaluator('2014-01-01', '2016-02-01', "KDJStrategy",
                                  symbols=IT_SYMBOLS, thread_number=1)
    evaluator.start()
    evaluator.dump_report()


if __name__ == "__main__":
    test_kdjstrategy("VMW")
    # evaluate_kdjstrategy()