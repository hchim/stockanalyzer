import pandas as pd
import numpy as np
import math

from utils.webdata import get_close_of_symbols, get_data_of_symbol
from utils.draw import plot_multi_symbols, normalize_data, plot_histogram, plot_scatter
from analysis.portfolio import find_optimal_allocations, get_portfolio_stats, get_portfolio_value
from analysis.basic import compute_daily_returns, analyze_market_correlation, evaluate_predict_result
from strategy.QStrategy import QStrategy
from learner.NaiveBayesLearner import NaiveBayesLearner
from simulator.TrendReverseEvaluator import CompositeTREvaluator


def test_webdata_multiple():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['AAPL', 'AMZN']
    prices = get_close_of_symbols(symbols, startdate, enddate)
    plot_multi_symbols(prices, normalize=True)


def test_portfolio_optimize():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['GOOG', 'AAPL', 'AMZN', 'FB']
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


def test_qstrategy():
    strategy = QStrategy({
        "RSI":{"window":14},
        # "MFI":None,
        # "CMF":None,
    })
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


def test_nbayes_learner():
    learner = NaiveBayesLearner()
    datax = [(0, 0),
             (0, 1),
             (0, 1),
             (0, 2),
             (1, 0),
             (1, 1),
             (1, 2),
             (1, 0)]
    datay = [1, 0, 1, 0, 1, 0, 1, 0]
    dates = pd.date_range("2016-01-01", "2016-01-08")
    datax = pd.DataFrame(datax, index=dates, columns=["A0", "A1"])
    learner.train(datax, pd.DataFrame(datay, index=dates, columns=["Y"]))
    print learner.query(datax)


if __name__ == "__main__":
    # test_webdata_multiple()
    test_portfolio_optimize()
    # test_market_correlation_analysis()
    # evaluate_strategy()
    # test_strategy()
    # test_qstrategy()
    # test_nbayes_learner()
    # test_candlestick_patterns()
    # test_nbayes_learner()