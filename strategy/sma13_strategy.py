import pandas as pd
import numpy as np

from analysis.indicators import sma, macd

DATE_FORMAT = '%Y-%m-%d'


def generate_sma13_orders(prices, symbol, start_value=1000000, save_to_file=False, filepath="sma13_orders.csv"):
    """
    Use the SMA13_MACD strategy to generate orders for the symbol.

    Parameters
    ----------
    prices: DataFrame
        the prices of the symbol
    symbol: string
        the symbol of the stock
    start_value: float
        the start value
    save_to_file: boolean
        save orders to file
    filepath: string
        file path

    Returns
    ----------
    orders: DataFrame
        the orders
    """
    if isinstance(prices, pd.DataFrame):
        prices = prices['Close']

    sma5 = sma(prices, 5)
    sma13 = sma(prices, 13)
    macd_val, signal, histogram = macd(prices)

    cash = start_value
    long_shares = 0
    dates = prices.index
    pre_ma5 = pre_ma13 = np.nan
    orders = []

    if save_to_file:
        file = open(filepath, 'w')
        file.write('Date,Symbol,Order,Shares\r\n')

    for date in dates:
        tmp_pre_ma5 = pre_ma5
        tmp_pre_ma13 = pre_ma13
        close = prices.loc[date]
        pre_ma5 = ma5 = sma5.loc[date]
        pre_ma13 = ma13 = sma13.loc[date]
        signal_v = signal.loc[date]

        if np.isnan(tmp_pre_ma13) or signal_v < 0:
            continue

        # long operations
        if long_shares == 0 and ma5 > tmp_pre_ma5 and ma13 > tmp_pre_ma13 and ma5 > ma13 and close > ma5:
            long_shares = round(cash / close, 0)
            cash -= long_shares * close
            if save_to_file:
                file.write("{0},{1},BUY,{2}\r\n".format(date.strftime(DATE_FORMAT), symbol, long_shares))
            orders.append((date, symbol, 'BUY', long_shares))
            continue

        if long_shares > 0 and close < ma5:
            cash += long_shares * close
            if save_to_file:
                file.write("{0},{1},SELL,{2}\r\n".format(date.strftime(DATE_FORMAT), symbol, long_shares))
            orders.append((date, symbol, 'SELL', long_shares))
            long_shares = 0
            continue

    df = pd.DataFrame(orders, columns=['Date', 'Symbol', 'Order', 'Shares'])
    return df