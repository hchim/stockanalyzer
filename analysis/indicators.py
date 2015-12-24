import pandas as pd


def sma(prices, window):
    """
    Calculate the simple moving average indicator

    Parameters
    ----------
    prices: Series or DataFrame
    window: int
        the window of the moving average

    Returns
    ----------
    sma_val : Series or DataFrame
        the simple moving average of the prices in the given window
    """
    return pd.rolling_mean(prices, window)


def ema(prices, window):
    """
    Calculate the exponential moving average indicator

    Parameters
    ----------
    prices: Series or DataFrame
    window: int
        the window of the exponential moving average

    Returns
    ----------
    ema_val: Series or DataFrame
        the exponential moving average of the prices in the given window
    """
    return pd.ewma(prices, span=window)


def bollinger_bands(prices):
    """
    Calculate the bollinger bands indicator

    Parameters
    ----------
    prices: Series or DataFrame

    Returns
    ----------
    rm: Series or DataFrame
        middle band
    upper_band : Series or DataFrame
    lower_band : Series or DataFrame
    """
    rm = pd.rolling_mean(prices, 20)   # 20 day mean
    rstd = pd.rolling_std(prices, 20)  # 20 day standard deviation
    upper_band = rm + (rstd * 2)
    lower_band = rm - (rstd * 2)

    return rm, upper_band, lower_band


def macd(prices):
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
    return macd_val, signal, histgram