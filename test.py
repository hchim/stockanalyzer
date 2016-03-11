import pandas as pd
import math

from utils.webdata import get_close_of_symbols, get_data_of_symbol
from utils.draw import plot_histogram, plot_scatter
from analysis.basic import compute_daily_returns, analyze_market_correlation, evaluate_predict_result
from strategy.QStrategy import QStrategy
from learner.NaiveBayesLearner import NaiveBayesLearner


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
    test_market_correlation_analysis()
    # test_qstrategy()
    # test_nbayes_learner()