"""
This file implements the functions that extract features from indicators.
"""
import numpy as np
import pandas as pd

from indicators import sma, ema, macd, kdj, cci, adx, stoch

"""
Trend Feature: it shows the current trend of the symbol.
    1: bull trend
    0: no trend
    -1: bear trend
"""
def trend_sma(prices, params):
    """
    Use the simple moving average values of two different periods
    to distinguish the current trend.

    Rules:
        1. bull trend if fast > slow
        2. bear trend if fast <= slow
    """
    sma_val = sma(prices, params=params)
    fast = sma_val.ix[:,0]
    slow = sma_val.ix[:,1]
    data = np.zeros(len(prices.index))

    for i in range(len(fast)):
        if np.isnan(slow[i]):
            continue

        if fast[i] > slow[i]:
            data[i] = 1
        else:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def trend_ema(prices, params):
    ema_val = ema(prices, params=params)
    fast = ema_val.ix[:,0]
    slow = ema_val.ix[:,1]
    data = np.zeros(len(prices.index))

    for i in range(len(fast)):
        if np.isnan(slow[i]):
            continue

        if fast[i] > slow[i]:
            data[i] = 1
        else:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def trend_macd_zero_line(prices, params=None):
    """
    Use diff and dea of the macd indicator to find out the trend.

    Rules:
        1. bull : diff > 0 and diff > dea
        2. bear : diff <= 0 and diff < dea
        3. otherwise, unknown
    """
    macd_val = macd(prices)
    diff = macd_val["DIFF"]
    data = np.zeros(len(prices.index))

    for i in range(len(prices.index)):
        if diff[i] > 0:
            data[i] = 1
        elif diff[i] < 0:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def trend_adx(prices, params={"window": 14, "threshold": 20}):
    """
    Rules:
        1. bull : adx > 20 and +DI > -DI
        2. bear : adx > 20 and +DI < -DI
        3. otherwise, weak trend or no trend
    """
    adx_val = adx(prices, params)
    pdi = adx_val["+DI"]
    mdi = adx_val["-DI"]
    adx_val = adx_val["ADX"]
    data = np.zeros(len(prices.index))

    for i in range(len(prices.index)):
        if np.isnan(adx_val[i]) or np.isnan(pdi[i]) or np.isnan(mdi[i]):
            continue

        if adx_val[i] > params["threshold"]:
            if pdi[i] > mdi[i]:
                data[i] = 1
            else:
                data[i] = -1

    return pd.Series(data, index=prices.index)


def trend_stoch(prices, params={"windows": [14, 3, 3]}):
    stoch_val = stoch(prices, params)

    k = stoch_val["K"]
    d = stoch_val["D"]
    data = np.zeros(len(prices.index))

    for i in range(len(prices.index)):
        if np.isnan(k[i]) or np.isnan(d[i]):
            continue

        if k[i] > d[i]:
            data[i] = 1
        else:
            data[i] = -1

    return pd.Series(data, index=prices.index)


"""
Reverse Feature: it shows the price may increase or decrease.
    1: bull signal
    0: unknown
    -1: bear
"""

def reverse_kdj_over_sell_buy(prices, params={"thresholds": [0, 100]}):
    if not "windows" in params:
        kdj_val = kdj(prices)
    else:
        kdj_val = kdj(prices, params)
    thresholds = params["thresholds"]
    data = np.zeros(len(prices.index))
    j_val = kdj_val["J"]

    for i in range(len(prices.index)):
        if np.isnan(j_val[i]):
            continue

        if j_val[i - 1] < thresholds[0] and j_val[i] > thresholds[0]:
            data[i] = 1
        elif j_val[i - 1] > thresholds[1] and j_val[i] < thresholds[1]:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def reverse_kdj_cross(prices, params={"thresholds": [30, 70]}):
    if not "windows" in params:
        kdj_val = kdj(prices)
    else:
        kdj_val = kdj(prices, params)
    thresholds = params["thresholds"]
    data = np.zeros(len(prices.index))
    k_val = kdj_val["K"]
    d_val = kdj_val["D"]

    for i in range(len(prices.index)):
        if k_val[i - 1] < d_val[i - 1] and k_val[i] >= d_val[i] and k_val[i] < thresholds[0]:
            data[i] = 1
        elif k_val[i - 1] > d_val[i - 1] and k_val[i] <= d_val[i] and k_val[i] > thresholds[1]:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def reverse_sma_cross(prices, params):
    """
    Use the cross signal of two the sma values of two different periods (fast and slow)
    as reverse signal.

    Rules:
        1. bull trend if fast crosses slow and fast > slow
        2. bear trend if fast crosses slow and fast < slow
    """
    sma_val = sma(prices, params=params)
    fast = sma_val.ix[:,0]
    slow = sma_val.ix[:,1]
    data = np.zeros(len(prices.index))

    for i in range(len(fast)):
        if np.isnan(slow[i]):
            continue

        if fast[i] > slow[i] and fast[i-1] <= slow[i-1]:
            data[i] = 1
        elif fast[i] < slow[i] and fast[i-1] >= slow[i-1]:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def reverse_ema_cross(prices, params):
    ema_val = ema(prices, params=params)
    fast = ema_val.ix[:,0]
    slow = ema_val.ix[:,1]
    data = np.zeros(len(prices.index))

    for i in range(len(fast)):
        if np.isnan(slow[i]):
            continue

        if fast[i] > slow[i] and fast[i-1] <= slow[i-1]:
            data[i] = 1
        elif fast[i] < slow[i] and fast[i-1] >= slow[i-1]:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def reverse_cci_over_sell_buy(prices, params=None):
    if params is None:
        cci_val = cci(prices)
    else:
        cci_val = cci(prices, params)
    cci_val = cci_val["CCI"]
    data = np.zeros(len(prices.index))

    for i in range(1, len(prices.index)):
        if cci_val[i - 1] < -200 and cci_val[i] > -200:
            data[i] = 1
        elif cci_val[i - 1] > 200 and cci_val[i] < 200:
            data[i] = -1

    return pd.Series(data, index=prices.index)


def reverse_cci_cross(prices, params=None):
    if params is None:
        cci_val = cci(prices)
    else:
        cci_val = cci(prices, params)
    cci_val = cci_val["CCI"]
    data = np.zeros(len(prices.index))

    for i in range(1, len(prices.index)):
        if cci_val[i - 1] < 100 and cci_val[i] > 100:
            data[i] = 1
        elif cci_val[i - 1] > -100 and cci_val[i] < -100:
            data[i] = -1

    return pd.Series(data, index=prices.index)