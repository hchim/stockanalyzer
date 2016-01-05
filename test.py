import pandas as pd
import numpy as np
import math

from utils.webdata import get_data_of_symbol, get_close_of_symbols
from utils.draw import plot_single_symbol, plot_multi_symbols, normalize_data, plot_histogram, plot_scatter
from analysis.portfolio import find_optimal_allocations, get_portfolio_stats, get_portfolio_value
from analysis.basic import compute_daily_returns, analyze_market_correlation, evaluate_predict_result
from analysis.normindicators import calculate_indicators
from strategy.SLStrategy import Strategy
from learner.BagLearner import BagLearner
from learner.KNNLearner import KNNLearner
from analysis.indicators import discritized_indicators
from strategy.QStrategy import QStrategy
from simulator.TradeSimulator import TradeSimulator


def test_webdata_multiple():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['AAPL', 'AMZN']
    prices = get_close_of_symbols(symbols, startdate, enddate)
    plot_multi_symbols(prices, normalize=True)


def test_webdata_single():
    startdate = '2015-05-15'
    enddate = '2015-12-23'
    prices = get_data_of_symbol('AAPL', startdate, enddate, fill_empty=False)
    plot_single_symbol(prices, indicators={
        "VOLUME" : None,
        # "BB" : None,
        # "MACD" : None,
        "SMA5" : None,
        # "RSI" : None,
        # "MFI" : None,
        # "CMF" : None,
    })


def test_portfolio_optimize():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['GOOG', 'AAPL', 'AMZN', 'FB']
#    symbols = ['BABA', 'JD', 'VIPS', 'JMEI']
    prices_all = get_close_of_symbols(symbols, startdate, enddate)  # automatically adds SPY
    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # get optimal allocations
    allocs = find_optimal_allocations(prices)
    allocs = allocs / np.sum(allocs)  # normalize allocations

    port_val = get_portfolio_value(prices, allocs)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    # Print statistics
    print "Symbols:", symbols
    print "Optimal allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility:", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    normed_SPY = normalize_data(prices_SPY)
    df_temp = pd.concat([port_val, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_multi_symbols(df_temp, title="Daily Portfolio Value and SPY")


def test_market_correlation_analysis():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['JMEI', 'BABA']
    prices = get_close_of_symbols(symbols, startdate, enddate)
    beta, alpha, corr = analyze_market_correlation(prices, 'JMEI')
    print "Beta: ", beta
    print "Alpha: ", alpha
    print "Correlation Coefficiency: ", corr

    daily_return = compute_daily_returns(prices)
    plot_histogram(daily_return)
    plot_scatter(daily_return, beta, alpha, 'JMEI')


def test_normalized_indicators():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol("AAPL", startdate, enddate)
    indicators = calculate_indicators(prices,
                                      {
                                          "BB": None,
                                          "MOM":{"window":12},
                                          "CMF":None,
                                      })
    print indicators


def test_strategy():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol("AAPL", startdate, enddate)
    symbol="AAPL"
    indicators = {"BB": None, "MOM":{"window":12}}

    # compute how much of the data is training and testing
    train_rows = math.floor(0.8 * len(prices))
    test_rows = len(prices) - train_rows

    learner = BagLearner("KNN", {"k" : 5}, bags=20, percent=0.9)
    strategy = Strategy(indicators, learner)
    strategy.train_learner(prices.iloc[:train_rows+5,:])
    orders = strategy.generate_orders("AAPL", prices, test_rows, save_to_file=True, filepath="./out/orders.csv")

    plot_single_symbol(prices, indicators={
        "BB" : None
    }, orders=orders)

    # Process orders
    simulator = TradeSimulator()
    portvals = simulator.compute_portvals("2015-10-14", enddate, orders=orders)

    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals[portvals.columns[0]])

    # Print statistics
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility:", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    prices_SPY = get_close_of_symbols([], "2015-10-14", enddate)
    df_temp = pd.concat([portvals, prices_SPY], axis=1)
    plot_multi_symbols(normalize_data(df_temp), title="{} and SPY".format(symbol))


def evaluate_strategy():
    startdate = '2014-01-01'
    enddate = '2015-12-28'
    prices = get_data_of_symbol("AAPL", startdate, enddate)
    indicators = {"CMF":None, "SMA5": None}
    # compute how much of the data is training and testing
    train_rows = math.floor(0.6 * len(prices))
    test_rows = len(prices) - train_rows

    learner = BagLearner("KNN", {"k" : 5}, bags=10, percent=0.8, boost=True)
    strategy = Strategy(indicators, learner)
    strategy.train_learner(prices.iloc[:train_rows+5,:])

    testy = strategy.calculate_y(prices).values[-test_rows:-5]
    predy = strategy.predict(prices, test_rows)[:-5]

    rmse, corr = evaluate_predict_result(testy, predy)
    print "RMSE: ", rmse
    print "corr: ", corr[0,1]

    strategy.plot_data()


def test_discritized_indicators():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol("AAPL", startdate, enddate)
    indicators = discritized_indicators(prices,
                                      {
                                          "MFI": None,
                                          "RSI":{"window":14},
                                          "CMF":None,
                                      }, 10)
    print indicators


def test_qstrategy():
    strategy = QStrategy({
        "RSI":{"window":14},
        # "MFI":None,
        # "CMF":None,
    }, 10)
    startdate = '2010-01-01'
    enddate = '2015-12-28'
    prices = get_data_of_symbol("AAPL", startdate, enddate)

    # compute how much of the data is training and testing
    train_rows = math.floor(0.85 * len(prices))
    test_rows = len(prices) - train_rows
    strategy.train_learner(prices.iloc[:train_rows,:])
    strategy.plot_data()
    # predict = strategy.predict(prices, test_rows)
    # predict = predict['Action']
    # print predict[predict < 2]


if __name__ == "__main__":
    test_webdata_single()
    # test_webdata_multiple()
    # test_portfolio_optimize()
    # test_market_correlation_analysis()
    # test_normalized_indicators()
    # evaluate_strategy()
    # test_strategy()
    # test_discritized_indicators()
    # test_qstrategy()