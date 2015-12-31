import pandas as pd
import numpy as np


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


def rsi(prices, window=14):
    """
    Calculate the RSI indicator.

    Parameters
    ----------
    prices: DataFrame
    window: int

    Returns
    ----------
    rsi_val: DataFrame
    """
    delta = prices - prices.shift(1)  # the difference between rows
    gain = delta[delta > 0]  # gain
    lose = delta[delta < 0]  # lose
    data = pd.concat([delta.iloc[1:], gain, lose], axis=1)
    data.fillna(0, inplace=True) # fill NAN values
    data = pd.rolling_mean(data, window)  # average daily gain and lose
    rs = data.iloc[:, 1] / data.iloc[:,2] * -1
    rsi_val = 100 - 100 / (1 + rs)
    return rsi_val


def cmf(prices):
    """
    1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low)
    2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
    3. 20-period CMF = 20-period Sum of Money Flow Volume / 20 period Sum of Volume

    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.

    Returns
    ----------
    cmf_val: DataFrame
    """
    mfm = ((prices['Close'] - prices['Low']) - (prices['High'] - prices['Close'])) \
          /(prices['High'] - prices['Low'])
    mfv = mfm * prices['Volume']
    mfv = pd.rolling_sum(mfv, 20)
    volumes = pd.rolling_sum(prices['Volume'], 20)
    return (mfv/volumes).to_frame()


def mfi(prices):
    """
    1. Typical Price = (High + Low + Close)/3
    2. Raw Money Flow = Typical Price x Volume
    3. Money Flow Ratio = (14-period Positive Money Flow)/(14-period Negative Money Flow)
    4. Money Flow Index = 100 - 100/(1 + Money Flow Ratio)

    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.

    Returns
    ----------
    mfi_val: DataFrame
    """
    tp = (prices['High'] + prices['Low'] + prices['Close']) / 3.0
    rmf = tp * prices['Volume']
    prmf = rmf.copy()
    nrmf = rmf.copy()
    for date in prices.index:
        if prices.loc[date, 'Close'] >= prices.loc[date, 'Open']:
            nrmf[date] = 0
        else:
            prmf[date] = 0

    mfr = pd.rolling_sum(prmf, 14)/pd.rolling_sum(nrmf, 14)
    mfi_val = 100 - 100. / (1 + mfr)
    return mfi_val.to_frame()