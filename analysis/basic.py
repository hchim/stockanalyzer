import numpy as np
import pandas as pd
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

    return rmse, corr[0, 1]


def normalize(values):
    """
    Normalize the values.
    """
    return (values - values[0]) / values[0]


def daily_prices_to_weekly_prices(prices):
    data = []
    new_indices = []
    indices = prices.index

    start_ind = 0
    pre_week = indices[0].isocalendar()[1]
    for i in range(1, len(prices.index)):
        week = indices[i].isocalendar()[1]
        if week == pre_week:
            continue
        week_prices = prices.iloc[start_ind:i]
        new_indices.append(indices[i-1])
        data.append([week_prices["Open"][0],        # open
                    np.max(week_prices["High"]),    # high
                    np.min(week_prices["Low"]),     # low
                    week_prices["Close"][-1],       # close
                    np.sum(week_prices["Volume"])]) # volume
        start_ind = i
        pre_week = week

    df = pd.DataFrame(data, columns=["Open", "High", "Low", "Close", "Volume"], index=new_indices)
    return df