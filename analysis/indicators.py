import pandas as pd


def sma(prices, window):
    """
    Calculate the simple moving average indicator
    :param prices: Series or DataFrame type, the prices
    :param window: the window of the moving average
    :return: the simple moving average of the prices in the given window
    """
    return pd.rolling_mean(prices, window)


def ema(prices, window):
    """
    Calculate the exponential moving average indicator
    :param prices: Series or DataFrame type, the prices
    :param window: the window of the exponential moving average
    :return: the exponential moving average of the prices in the given window
    """
    return pd.ewma(prices, span=window)


def bollinger_bands(prices):
    """
    Calculate the bollinger bands indicator
    :param prices: Series or DataFrame type, the prices
    :return: middle band, upper band and lower band
    """
    rm = pd.rolling_mean(prices, 20)   # 20 day mean
    rstd = pd.rolling_std(prices, 20)  # 20 day standard deviation
    upper_band = rm + (rstd * 2)
    lower_band = rm - (rstd * 2)

    return rm, upper_band, lower_band


def macd(prices):
    """
    calculate the MACD indicator
    :param prices:   Series or DataFrame type, the prices
    :return: macd, signal and histgram
    """
    ema12 = ema(prices, 12)
    ema26 = ema(prices, 26)
    macd_val = ema12 - ema26
    signal = ema(macd_val, 9)
    histgram = macd_val - signal
    return macd_val, signal, histgram