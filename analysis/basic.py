import numpy as np
import math


def compute_daily_returns(prices):
    """
    Compute the daily return of the prices.
    """
    dr = (prices / prices.shift(1)) - 1
    dr.iloc[0] = 0
    return dr


def analyze_market_correlation(prices, symbol, index_symbol='SPY'):
    """
    Analyze the market correlation of the stock.

    Parameters
    ----------
    prices: DataFrame
        Close prices of the stock and the market index.
    symbol: stock symbol
    index_symbol: market index

    Returns
    ----------
    beta : float
    alpha : float
    corr : correlation coefficiency
    """
    daily_return = compute_daily_returns(prices)
    beta, alpha = np.polyfit(daily_return[index_symbol], daily_return[symbol], 1)
    corr = daily_return.corr(method='pearson')

    return beta, alpha, corr


def evaluate_predict_result(test, predict):
    """
    Calculate the metrics that evaluate the predict result.

    Pamameters
    -----------
    test: np.array
    predict: np.array

    Returns
    -----------
    rmse: float
        root-mean-squre error
    corr: float
        correlation coefficiency
    """
    rmse = math.sqrt(((test - predict) ** 2).sum()/test.shape[0])
    corr = np.corrcoef(predict, y=test)

    return rmse, corr