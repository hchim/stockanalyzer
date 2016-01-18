import pandas as pd
import pandas_datareader.data as web

from pandas_datareader._utils import RemoteDataError


def get_data_of_symbol(symbol, start, end, fill_empty=True):
    """
    Get the daily prices of the symbol in the specified range.

    Parameters
    ----------
    symbol: string
        the symbol of the stock
    start: string
        the start date
    end: string
        the end date

    Returns
    ----------
    df: DataFrame
        it contains the columns [Open, High, Low, Close, Volume]
    """
    try:
        df = web.DataReader(symbol, 'google', start, end)
    except RemoteDataError as err:
        print "Failed to to get the data of symbol: ", symbol
        print err.strerror
        return None

    # fill empty values
    if fill_empty:
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='backfill', inplace=True)

    return df


def get_close_of_symbols(symbols, start, end, add_spy=True, fill_empty=True):
    """
    Get the adj close prices of the symbols. Add SPY by default.
    Parameters
    ----------
    symbols: list
        the symbols of the stocks
    start: string
        the start date
    end: string
        the end date
    add_spy: add SPY to the data

    Returns
    ----------
    df: DataFrame
        the adj close prices of the stocks
    """
    dates = pd.date_range(start, end)
    df = pd.DataFrame(index=dates)
    if add_spy and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = symbols + ['SPY']

    for symbol in symbols:
        df_temp = get_data_of_symbol(symbol, start, end, fill_empty=False)
        if df_temp is None:
            continue

        df_temp = df_temp['Close'].to_frame()   # get the 'adj close' column and convert to DataFrame
        df_temp.rename(columns={'Close': symbol}, inplace=True)
        df = df.join(df_temp)

    if add_spy:  # drop dates that SPY has no trades
        df.dropna(subset=["SPY"], inplace=True)

    # fill empty values
    if fill_empty:
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='backfill', inplace=True)
    return df