import pandas as pd
import numpy as np

def discritizing(values, v_range, bin_num):
    """
    Discritize the values.

    Parameters
    ----------
    values: Series
    v_range: tuple
        the range of the values.
    bin_num: int

    Returns
    ---------
    inds: Series
        The values are between 0 and bin_num - 1.
    """
    if isinstance(values, pd.DataFrame):
        values = values.iloc[:, 0]

    stepsize = (v_range[1] - v_range[0]) * 1.0 / bin_num
    bins = np.arange(v_range[0], v_range[1], step=stepsize)
    inds = np.digitize(values, bins) - 1
    df = pd.DataFrame(inds, index=values.index)
    return df


def discritized_indicators(prices, params, bin_num):
    """
    Calculate the discritized indicators with the given prices.

    Parameters
    ----------
    prices: DataFrame
    params: map
        The keys of the map are the names of the indicators. The values of the map are
        the parameters to calculate the indicators.
    bin_num: int
        The number of bins.

    Returns
    ----------
    dist_indicator: DataFrame
    """
    indicators = pd.DataFrame(index=prices.index)
    close = prices['Close']

    for name in params.keys():
        values = None
        inds = None
        if name == "RSI":
            values = rsi(close, params[name]["window"])
            values.dropna(inplace=True)
            inds = discritizing(values, (0, 100), bin_num)
        elif name == "CMF":
            values = cmf(prices)
            values.dropna(inplace=True)
            inds = discritizing(values, (-1, 1), bin_num)
        elif name == "MFI":
            values = mfi(prices)
            values.dropna(inplace=True)
            inds = discritizing(values, (0, 100), bin_num)

        if inds is not None:
            indicators = indicators.join(inds)
            indicators.rename(columns={indicators.columns[-1]:name}, inplace=True)

    indicators.dropna(inplace=True)
    dist_indicator = indicators.iloc[:, 0]
    for col in indicators.columns[1:]:
        dist_indicator = dist_indicator * bin_num + indicators[col]

    return dist_indicator


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
    dist_indicator: DataFrame
    """
    indicators = pd.DataFrame(index=prices.index)
    close = prices['Close']

    for name in params.keys():
        values = None
        if name == "RSI":
            values = rsi(close, params[name]["window"])
        elif name == "CMF":
            values = cmf(prices)
        elif name == "MFI":
            values = mfi(prices)
        elif name == "BB":
            rm, upper, lower = bollinger_bands(close)
            values = pd.DataFrame(index=rm.index, columns=["BB_Middle", "BB_Upper", "BB_Lower"])
            values.loc[:, "BB_Middle"] = rm
            values.loc[:, "BB_Upper"] = upper
            values.loc[:, "BB_Lower"] = lower
        elif name.startswith("SMA"):
            window = int(name[3:])
            values = sma(close, window)
        elif name.startswith("EMA"):
            window = int(name[3:])
            values = ema(close, window)
        elif name == "MACD":
            macd_val, signal, histgram = macd(close)
            values = pd.DataFrame(index=macd_val.index, columns=["MACD_Val", "MACD_Signal", "MACD_Histgram"])
            values.loc[:, "MACD_Val"] = macd_val
            values.loc[:, "MACD_Signal"] = signal
            values.loc[:, "MACD_Histgram"] = histgram

        if values is not None:
            indicators = indicators.join(values)

    indicators.dropna(inplace=True)
    return indicators


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
    sma_val = pd.rolling_mean(prices, window)
    if isinstance(sma_val, pd.Series):
        sma_val = sma_val.to_frame()

    sma_val.rename(columns={sma_val.columns[-1]:"SMA{}".format(window)}, inplace=True)
    return sma_val


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
    ema_val = pd.ewma(prices, span=window)
    if isinstance(ema_val, pd.Series):
        ema_val = ema_val.to_frame()

    ema_val.rename(columns={ema_val.columns[-1]:"EMA{}".format(window)}, inplace=True)
    return ema_val


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
    macd_val = ema12.iloc[:, 0] - ema26.iloc[:, 0]
    signal = ema(macd_val, 9).iloc[:, 0]
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
    rsi_val = rsi_val.to_frame()
    rsi_val.rename(columns={rsi_val.columns[-1]:"RSI"}, inplace=True)
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
    cmf_val = (mfv/volumes).to_frame()
    cmf_val.rename(columns={cmf_val.columns[-1]:"CMF"}, inplace=True)
    return cmf_val


def __tp(prices):
    return (prices['High'] + prices['Low'] + prices['Close']) / 3.0


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
    tp = __tp(prices)
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
    mfi_val = mfi_val.to_frame()
    mfi_val.rename(columns={mfi_val.columns[-1]:"MFI"}, inplace=True)
    return mfi_val


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
    """
    tr = __tr(prices)
    window = params["window"]
    length = len(prices.index)
    atr_val = pd.Series(np.zeros(length), index=prices.index)
    atr_val[1] = tr[1]

    for i in range(2, length):
        atr_val[i] = (atr_val[i-1] * (window - 1) + tr[i]) / window
    return atr_val


def adx(prices, params={"window":14}):
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

    str = __wilder_smooth_1(tr, window=params["window"])
    spdm = __wilder_smooth_1(pdm, window=params["window"])
    smdm = __wilder_smooth_1(mdm, window=params["window"])
    # green line
    pdi = spdm / str * 100
    # red line
    mdi = smdm / str * 100
    dx = abs(pdi - mdi) / (pdi + mdi) * 100
    adx_val = __wilder_smooth_2(dx, window=params["window"])
    return adx_val, pdi, mdi


def cci(prices, params={"window":20}):
    length = len(prices.index)
    window = params["window"]

    tp = __tp(prices)
    stp = pd.rolling_mean(tp, window)
    cci_val = pd.Series(np.zeros(length), index=prices.index)
    cci_val[0:window-1] = np.nan

    for i in range(window-1, length):
        dev = np.sum(abs(stp[i] - tp[i-window+1:i+1])) / window
        cci_val[i] = (tp[i]  -  stp[i]) / (0.015 * dev)

    return cci_val
