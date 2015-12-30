import numpy as np
import pandas as pd

from analysis.basic import compute_daily_returns
from analysis.indicators import ema

"""
The package defines the algorithms that calculate the normalized indicators.
"""

def calculate_indicators(prices, params):
    """
    Calculate the indicators with the given prices.

    Parameters
    ----------
    prices: DataFrame
    params: map
        The keys of the map are the names of the indicators. The values of the map are
        the parameters to calculate the indicators.

    Returns
    ----------
    indicators: DataFrame
    """
    indicators = pd.DataFrame(index=prices.index)
    close = prices['Close']

    for name in params.keys():
        values = None
        if name == "BB":
            values = norm_bollinger_bands(close)
        elif name == "MOM":
            values = norm_momentum(close, params[name])
        elif name == "RSI":
            values = norm_rsi(close, params[name])
        elif name == "VOL":
            values = norm_volatility(close)
        elif name.startswith("SMA"):
            window = int(name[3:])
            values = norm_sma(close, window)
        elif name.startswith("EMA"):
            window = int(name[3:])
            values = norm_ema(close, window)
        elif name == "MACD":
            values = norm_macd(close)

        if values is not None:
            indicators = indicators.join(values)
            indicators.rename(columns={indicators.columns[-1]:name}, inplace=True)

    return indicators


def norm_bollinger_bands(prices):
    """
    bb_value[t] = (price[t] - SMA[t])/(2 * stdev[t])
    """
    rm = pd.rolling_mean(prices, 20)   # 20 day mean
    rstd = pd.rolling_std(prices, 20)  # 20 day standard deviation
    bb = (prices - rm)/ (2 * rstd)
    return bb


def norm_momentum(prices, params={"window":12}):
    """
    momentum[t] = (price[t]/price[t-N]) - 1
    """
    return prices/prices.shift(params["window"]) - 1


def norm_volatility(prices):
    """
    The standard deviation of daily return.
    """

    daily_return = compute_daily_returns(prices)
    vols = []
    for i in range(len(daily_return)):
        vols.append(daily_return.iloc[:i].std())
    return pd.DataFrame(data=vols, index=prices.index)


def norm_cmf(prices):
    """
    1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low)
    2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
    3. 20-period CMF = 20-period Sum of Money Flow Volume / 20 period Sum of Volume
    """
    pass


def norm_rsi(prices, params={"window":14}):
    """
    Calculate the RSI indicator and normalize the range to [-1, 1].

    Parameters
    ----------
    prices: DataFrame
    params: map

    Returns
    ----------
    rsi_val: DataFrame
    """
    delta = prices - prices.shift(1)  # the difference between rows
    gain = delta[delta > 0]  # gain
    lose = delta[delta < 0]  # lose
    data = pd.concat([delta.iloc[1:], gain, lose], axis=1)
    data.fillna(0, inplace=True) # fill NAN values
    data = pd.rolling_mean(data, params["window"])  # average daily gain and lose
    rs = data.iloc[:, 1] / data.iloc[:,2] * -1
    rsi_val = (50. - 100. / (1 + rs)) / 50.
    return rsi_val


def norm_sma(prices, window):
    rm = pd.rolling_mean(prices, window)
    return normalize_indicator(rm)


def norm_ema(prices, window):
    vals = ema(prices, window)
    return normalize_indicator(vals)


def norm_macd(prices):
    """
    Calculate the MACD indicator

    Parameters
    ----------
    prices: Series or DataFrame

    Returns
    ----------
    macd_val: Series or DataFrame
        macd values
    signal: Series or DataFrame
        signal values
    histgram: Series or DataFrame
        histgram values
    """
    ema12 = ema(prices, 12)
    ema26 = ema(prices, 26)
    macd_val = ema12 - ema26
    signal = ema(macd_val, 9)
    histgram = macd_val - signal
    return normalize_indicator(histgram)


def normalize_indicator(values):
    mean = values.mean()
    std = values.std()
    return (values - mean) / std