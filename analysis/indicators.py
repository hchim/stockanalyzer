import pandas as pd
import numpy as np


def sma(prices, params):
    """
    Calculate the simple moving average indicator.

    Parameters
    ----------
    prices: DataFrame
    params: dict
            e.g. {"windows": [5, 10]}

    Returns
    ----------
    sma_val : DataFrame
        the simple moving average of the close price.
    """
    windows = params["windows"]
    close = prices["Close"].values
    values = []
    column_names = []

    for w in windows:
        values.append(pd.rolling_mean(close, w))
        column_names.append("SMA{}".format(w))

    return pd.DataFrame(np.column_stack(tuple(values)), index=prices.index, columns=column_names)


def __ema(close, window):
    data = pd.ewma(close, span=window)
    data[0:window-1] = np.nan
    return data


def ema(prices, params):
    """
    Calculate the exponential moving average indicator.

    Parameters
    ----------
    prices: DataFrame
    params: dict
            e.g. {"windows": [5, 10]}

    Returns
    ----------
    ema_val : DataFrame
        the simple moving average of the close price.
    """
    windows = params["windows"]
    close = prices["Close"].values
    values = []
    column_names = []

    for w in windows:
        values.append(__ema(close, w))

        column_names.append("EMA{}".format(w))

    return pd.DataFrame(np.column_stack(tuple(values)), index=prices.index, columns=column_names)


def bb(prices, params={"window": 20}):
    """
    Calculate the bollinger bands indicator

    Parameters
    ----------
    prices: DataFrame
    params: dict

    Returns
    ----------
    bb_vals: DataFrame
    """
    window = params["window"]

    close = prices["Close"].values
    rm = pd.rolling_mean(close, window)   # 20 day mean
    rstd = pd.rolling_std(close, window)  # 20 day standard deviation
    upper_band = rm + (rstd * 2)
    lower_band = rm - (rstd * 2)
    values = np.column_stack((rm, upper_band, lower_band))
    return pd.DataFrame(values, index=prices.index, columns=["Middle", "Upper", "Lower"])


def macd(prices, params={"windows": [12, 26, 9]}):
    """
    Calculate the MACD indicator

    Parameters
    ----------
    prices: DataFrame
    params: dict

    Returns
    ----------
    macd_val: DataFrame
    """
    close = prices["Close"]
    windows = params["windows"]

    ema12 = __ema(close, windows[0])
    ema26 = __ema(close, windows[1])
    diff = ema12 - ema26
    dea = __ema(diff, windows[2])
    macd_val = diff - dea

    values = np.column_stack((diff, dea, macd_val))
    return pd.DataFrame(values, index=prices.index, columns=["DIFF", "DEA", "MACD"])


def rsi(prices, params={"window": 14}):
    """
    Calculate the RSI indicator.

    Parameters
    ----------
    prices: DataFrame
    params: dict

    Returns
    ----------
    rsi_val: DataFrame
    """
    window = params["window"]
    close = prices["Close"]

    delta = close - close.shift(1)  # the difference between rows
    gain = delta[delta > 0]  # gain
    lose = delta[delta < 0]  # lose
    data = pd.concat([delta, gain, lose], axis=1)
    data.fillna(0, inplace=True) # fill NAN values
    data = pd.rolling_mean(data, window)  # average daily gain and lose

    rs = data.iloc[:, 1] / data.iloc[:,2] * -1
    rsi_val = 100 - 100 / (1 + rs)
    return pd.DataFrame(rsi_val.values, index=prices.index, columns=["RSI"])


def __mfm(prices):
    mfm = ((prices['Close'] - prices['Low']) - (prices['High'] - prices['Close'])) \
          /(prices['High'] - prices['Low'])
    return mfm


def __mfv(prices):
    mfm = __mfm(prices)
    return mfm * prices['Volume']


def cmf(prices, params={"window": 20}):
    """
    1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low)
    2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
    3. 20-period CMF = 20-period Sum of Money Flow Volume / 20 period Sum of Volume

    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.
    params: dict

    Returns
    ----------
    cmf_val: DataFrame
    """
    window = params["window"]
    mfv = __mfv(prices)
    mfv = pd.rolling_sum(mfv, window)
    volumes = pd.rolling_sum(prices['Volume'], window)
    cmf_val = (mfv/volumes)

    return pd.DataFrame(cmf_val.values, index=prices.index, columns=["CMF"])


def __tp(prices):
    return (prices['High'] + prices['Low'] + prices['Close']) / 3.0


def mfi(prices, params={"window": 14}):
    """
    1. Typical Price = (High + Low + Close)/3
    2. Raw Money Flow = Typical Price x Volume
    3. Money Flow Ratio = (14-period Positive Money Flow)/(14-period Negative Money Flow)
    4. Money Flow Index = 100 - 100/(1 + Money Flow Ratio)

    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.
    params: dict

    Returns
    ----------
    mfi_val: DataFrame
    """
    window = params["window"]
    tp = __tp(prices)
    rmf = tp * prices['Volume']
    prmf = rmf.copy()
    nrmf = rmf.copy()
    for date in prices.index:
        if prices.loc[date, 'Close'] >= prices.loc[date, 'Open']:
            nrmf[date] = 0
        else:
            prmf[date] = 0

    mfr = pd.rolling_sum(prmf, window)/pd.rolling_sum(nrmf, window)
    mfi_val = 100 - 100. / (1 + mfr)

    return pd.DataFrame(mfi_val.values, index=prices.index, columns=["MFI"])


def __rsv(prices, window):
    close = prices["Close"]
    high = prices["High"]
    low = prices["Low"]
    length = len(prices.index)

    rsv_val = np.zeros(length)
    rsv_val[0:window-1] = np.nan

    for i in range(window-1, length):
        hn = high[i-window+1:i+1].max()
        ln = low[i-window+1:i+1].min()
        rsv_val[i] = (close[i] - ln) * 100.0 / (hn - ln)

    return rsv_val


def kdj(prices, params={"windows": [9, 3, 3]}):
    """
    Calculate KDJ indicator:
    RSV = (Ct - Ln) / (Hn - Ln) * 100
    K = sma3(RSV)
    D = sma3(K)
    J = 3 * D - 2 * K

    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.
    params: dict

    Returns
    ----------
    kdj_val: DataFrame
    """
    windows = params["windows"]
    rsv = __rsv(prices, windows[0])
    k = pd.rolling_mean(rsv, windows[1])
    d = pd.rolling_mean(k, windows[2])
    j = 3 * k - 2 * d
    kdj_val = np.column_stack((k, d, j))

    return pd.DataFrame(kdj_val, index=prices.index, columns=["K", "D", "J"])


def stoch(prices, params={"windows": [14, 3, 3]}):
    """
    RSV = (Ct - Ln) / (Hn - Ln) * 100
    K = sma(RSV, params["windows"][1])
    D = sma(K, params["windows"][2])

    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.
    params: dict

    Returns
    ----------
    kd_val: DataFrame
    """
    windows = params["windows"]
    rsv = __rsv(prices, windows[0])
    k = pd.rolling_mean(rsv, windows[1])
    d = pd.rolling_mean(k, windows[2])
    stoch_val = np.column_stack((k, d))

    return pd.DataFrame(stoch_val, index=prices.index, columns=["K", "D"])

def __tr(prices):
    """
    TR is defined as the greatest of the following:
    Method 1: Current High less the current Low
    Method 2: Current High less the previous Close (absolute value)
    Method 3: Current Low less the previous Close (absolute value)
    """
    m1 = prices['High'] - prices['Low']
    m2 = abs(prices['High'] - prices['Close'].shift(1))
    m3 = abs(prices['Low'] - prices['Close'].shift(1))

    tr = pd.concat([m1, m2, m3], axis=1).max(axis=1)
    tr[0] = np.nan
    return tr


def __wilder_smooth_1(values, window):
    """
    First TR14 = Sum of first 14 periods of TR1
    Second TR14 = First TR14 - (First TR14/14) + Current TR1
    Subsequent Values = Prior TR14 - (Prior TR14/14) + Current TR1
    """
    length = len(values.index)
    smooth_val = pd.Series(np.zeros(length), index=values.index)
    smooth_val[0:window] = np.nan
    smooth_val[window] = np.sum(values[1:window+1].values)

    for i in range(window + 1, length):
        smooth_val[i] = (smooth_val[i-1] * (1 - 1.0 / window)) + values[i]
    return smooth_val


def __wilder_smooth_2(values, window):
    """
    First ADX14 = 14 period Average of DX
    Second ADX14 = ((First ADX14 x 13) + Current DX Value)/14
    Subsequent ADX14 = ((Prior ADX14 x 13) + Current DX Value)/14
    """
    start = window
    length = len(values.index)
    smooth_val = pd.Series(np.zeros(length), index=values.index)
    smooth_val[0:start + window - 1] = np.nan
    smooth_val[start + window - 1] = np.mean(values[start: start + window].values)

    for i in range(start + window, length):
        smooth_val[i] = (smooth_val[i-1] * (window - 1) + values[i]) / window
    return smooth_val


def atr(prices, params={"window":14}):
    """
    Current ATR = [(Prior ATR x 13) + Current TR] / 14
    Average True Range (ATR) is an indicator that measures volatility.

    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.
    params: dict

    Returns
    ----------
    atr_val: DataFrame
    """
    tr = __tr(prices)
    window = params["window"]
    length = len(prices.index)
    atr_val = pd.Series(np.zeros(length), index=prices.index)
    atr_val[1] = tr[1]

    for i in range(2, length):
        atr_val[i] = (atr_val[i-1] * (window - 1) + tr[i]) / window
    return pd.DataFrame(atr_val.values, index=prices.index, columns=["ATR"])


def adx(prices, params={"window":14}):
    """
    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.
    params: dict

    Returns
    ----------
    adx_val: DataFrame
        the DataFrame has three columns: ADX, +DI, -DI
    """
    window = params["window"]
    tr = __tr(prices)
    high = prices["High"]
    low = prices["Low"]
    length = len(prices.index)
    pdm = pd.Series(np.zeros(length), index=prices.index)
    mdm = pd.Series(np.zeros(length), index=prices.index)
    pdm[0] = np.nan
    mdm[0] = np.nan

    for i in range(1, length):
        up = high[i] - high[i-1]
        down = low[i-1] - low[i]

        if up > down and up > 0:
            pdm[i] = up

        if down > up and down > 0:
            mdm[i] = down

    str = __wilder_smooth_1(tr, window)
    spdm = __wilder_smooth_1(pdm, window)
    smdm = __wilder_smooth_1(mdm, window)
    # green line
    pdi = spdm / str * 100
    # red line
    mdi = smdm / str * 100
    dx = abs(pdi - mdi) / (pdi + mdi) * 100
    adx_val = __wilder_smooth_2(dx, window)
    values = np.column_stack((adx_val, pdi, mdi))
    return pd.DataFrame(values, index=prices.index, columns=["ADX", "+DI", "-DI"])


def cci(prices, params={"window":20}):
    """
    Parameters
    ----------
    prices: DataFrame
        Includes the open, close, high, low and volume.
    params: dict

    Returns
    ----------
    cci_val: DataFrame
    """
    length = len(prices.index)
    window = params["window"]

    tp = __tp(prices)
    stp = pd.rolling_mean(tp, window)
    cci_val = pd.Series(np.zeros(length), index=prices.index)
    cci_val[0:window-1] = np.nan

    for i in range(window-1, length):
        dev = np.sum(abs(stp[i] - tp[i-window+1:i+1])) / window
        cci_val[i] = (tp[i]  -  stp[i]) / (0.015 * dev)

    return pd.DataFrame(cci_val.values, index=prices.index, columns=["CCI"])


def obv(prices, params=None):
    length = len(prices.index)
    close = prices["Close"]
    volume = prices["Volume"]
    obv_val = pd.Series(np.zeros(length), index=prices.index)
    obv_val[0] = volume[0]

    for i in range(1, length):
        if close[i] > close[i-1]:
            obv_val[i] = obv_val[i-1] + volume[i]
        elif close[i] < close[i-1]:
            obv_val[i] = obv_val[i-1] - volume[i]
        else:
            obv_val[i] = obv_val[i-1]

    return pd.DataFrame(obv_val.values, index=prices.index, columns=["OBV"])


def adl(prices, params=None):
    """
    1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low)
    2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
    3. ADL = Previous ADL + Current Period's Money Flow Volume
    """
    length = len(prices.index)
    mfv = __mfv(prices)
    adl_val = pd.Series(np.zeros(length), index=prices.index)
    adl_val[0] = mfv[0]

    for i in range(1, length):
        adl_val[i] = adl_val[i-1] + mfv[i]

    return pd.DataFrame(adl_val.values, index=prices.index, columns=["ADL"])