import pandas as pd
import numpy as np

from utils.webdata import get_close_of_symbols


def compute_leverage(prices, shares, cash, order_type, order_share, order_symbol):
    """
    Compute the leverage of the shares

    Parameters
    ----------
    prices: Series
    shares: dict
        contains the current shares for each symbol
    cash: float
        current cash
    order_type: [BUY or SELL]
        the type of the order
    order_share: int
        the number of shares of the order
    order_symbol: string
        the symbol of the order

    Returns
    ----------
    leverage: float
    """
    if order_type == 'BUY':
        shares[order_symbol] += order_share
        cash -= prices[order_symbol] * order_share
    else:
        shares[order_symbol] -= order_share
        cash += prices[order_symbol] * order_share

    longs = shorts = 0
    for symbol in shares.keys():
        if shares[symbol] >= 0:
            longs += shares[symbol] * prices[symbol]
        else:
            shorts -= shares[symbol] * prices[symbol]

    leverage = (longs + shorts) / (longs - shorts + cash)
    return leverage


def compute_portvals(start_date, end_date, orders=None, orders_file=None, start_val=1000000, leverage=2.0, allow_short=True):
    """Simulate the trades with the given orders and the prices.

    Parameters
    ----------
    start_date: string
    end_date: string
    prices: DataFrame
    orders: DataFrame
    orders_file: string
    start_val: float
        start value of the portfolio
    leverage: float
        max leverage
    allow_short: boolean
        allows to sell short

    Returns
    ----------
    portvals: DataFrame
        the daily portfolio values in the simulation
    """
    if orders is None:
        orders = pd.read_csv(orders_file, parse_dates=True)

    symbols = list(set(orders['Symbol']))
    prices = get_close_of_symbols(symbols, start_date, end_date, add_spy=True) # add SPY so as to remove no-trade days
    prices.drop('SPY', axis=1, inplace=True)       # remove SPY

    dates = prices.index                           # update dates
    # init daily shares
    shares = prices.copy()                         # record the shares every day
    shares.loc[:, :] = np.nan
    last_share = dict.fromkeys(shares.columns, 0)  # record the total shares of each symbol
    # init daily cashes
    cashes = pd.Series({'Cash':np.nan}, index=dates) # record the daily cashes
    last_cash = start_val                          # record total cash

    # iterate orders and simulate the trades
    for i in range(len(orders)):
        symbol = orders.loc[i, 'Symbol']
        share = orders.loc[i, 'Shares']
        date = orders.loc[i, 'Date']
        operate = orders.loc[i, 'Order']
        price = prices.loc[date, symbol]

        # check leverage
        tmp_leverage = compute_leverage(prices.loc[date, :], last_share.copy(), last_cash,
                                        operate, share, symbol)
        if tmp_leverage > leverage:
            continue

        if operate == 'BUY':
            last_share[symbol] += share
            shares.loc[date, symbol] = last_share[symbol]
            val = last_cash - price * share
            cashes[date] = last_cash = val
        else:
            temp_share = last_share[symbol] - share
            # short check
            if not allow_short and temp_share < 0:
                continue
            shares.loc[date, symbol] = last_share[symbol] = temp_share
            last_cash += price * share
            cashes[date] = last_cash

    # init the nan values of the first row of shares before invoking fillna
    for symbol in shares.columns:
        if pd.isnull(shares.loc[dates[0], symbol]):
            shares.loc[dates[0], symbol] = 0

    shares.fillna(method="ffill", inplace=True)
    # init the nan value of the first row of cashes before invoking fillna
    if pd.isnull(cashes.ix[0]):
        cashes.ix[0] = start_val
    cashes.fillna(method='ffill', inplace=True)
    values = (prices * shares).sum(axis=1)
    portvals = (values + cashes).to_frame()
    portvals.rename(columns={portvals.columns[0]: "Portfolio"}, inplace=True)
    return portvals

