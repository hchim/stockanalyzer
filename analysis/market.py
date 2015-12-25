import numpy as np


def compute_daily_returns(prices):
    dr = (prices / prices.shift(1)) - 1
    dr.ix[0,:] = 0 # set first row to 0
    return dr


def analyze_market_correlation(prices, symbol, index_symbol='SPY'):
    """
    Analyze the market correlation of the stock.

    Parameters
    ----------
    prices: DataFrame
        Adj close prices of the stock and the market index.
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