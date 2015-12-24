import numpy as np
import pandas as pd

from analysis.indicators import bollinger_bands

DATE_FORMAT = '%Y-%m-%d'


def generate_bb_orders(prices, symbol, allow_short=True, start_value=1000000, save_to_file=False, filepath="bb_orders.csv"):
    """
    A basic Bollinger Band trading strategy works as follows: There are two potential entries, long and short.
    The long entry is made when the price transitions from below the lower band to above the lower band. This
    indicates that the stock price has moved substantially away from the moving average, but is now moving back
    towards the moving average. When this entry signal criteria is met, buy the stock and hold it until the exit.
    The exit signal occurs when the price moves from below the SMA to above it.

    The short entry and exit are mirrors of the long entry and exit: The short entry is made when the price
    transitions from above the upper band to below the upper band. This indicates that the stock price has
    moved substantially away from the moving average, but is now moving back towards the moving average.
    When this entry signal criteria is met, short the stock and hold it until the exit. The exit signal
    occurs when the price moves from above the SMA to below it.

    Parameters
    ----------
    prices: DataFrame
        the prices of the symbol
    symbol: string
        the symbol of the stock
    allow_short: boolean
        allow short
    start_value: float
        start value
    save_to_file: boolean
        save orders to file
    filepath: boolean
        file path

    Returns
    ----------
    orders: DataFrame
    """
    if isinstance(prices, pd.DataFrame):
        prices = prices['Adj Close']

    sma20, upper_band, lower_band = bollinger_bands(prices)
    cash = start_value
    long_shares = short_shares = 0
    dates = prices.index
    pre_close = prices.loc[dates[0]]
    orders = []

    if save_to_file:
        file = open(filepath, 'w')
        file.write('Date,Symbol,Order,Shares\r\n')

    for date in dates:
        if np.isnan(lower_band.loc[date]):
            continue

        tmp_pre_close = pre_close
        close = prices.loc[date]
        pre_close = close
        lower = lower_band.loc[date]
        upper = upper_band.loc[date]
        middle = sma20.loc[date]

        # long operations
        if long_shares == 0 and tmp_pre_close < lower and close > lower:
            long_shares = round(cash / close, 0)
            cash -= long_shares * close
            if save_to_file:
                file.write("{0},{1},BUY,{2}\r\n".format(date.strftime(DATE_FORMAT), symbol, long_shares))
            orders.append((date, symbol, 'BUY', long_shares))
            continue

        if long_shares > 0 and tmp_pre_close < middle and close > middle:
            cash += long_shares * close
            if save_to_file:
                file.write("{0},{1},SELL,{2}\r\n".format(date.strftime(DATE_FORMAT), symbol, long_shares))
            orders.append((date, symbol, 'SELL', long_shares))
            long_shares = 0
            continue

        if not allow_short:
            continue

        if short_shares == 0 and tmp_pre_close > upper and close < upper:
            short_shares = round(cash / close, 0)
            cash += short_shares * close
            if save_to_file:
                file.write("{0},{1},SELL,{2}\r\n".format(date.strftime(DATE_FORMAT), symbol, short_shares))
            orders.append((date, symbol, 'SELL', short_shares))
            continue

        if short_shares > 0 and tmp_pre_close > middle and close < middle:
            cash -= short_shares * close
            if save_to_file:
                file.write("{0},{1},BUY,{2}\r\n".format(date.strftime(DATE_FORMAT), symbol, short_shares))
            orders.append((date, symbol, 'BUY', short_shares))
            short_shares = 0

    df = pd.DataFrame(orders, columns=['Date', 'Symbol', 'Order', 'Shares'])
    return df
