import pandas as pd
import pandas.io.data as web


def get_data_of_symbol(symbol, start, end, fill_empty=True):
    """
    Get the daily prices of the symbol in the specified range.
    :param symbol: the symbol of the stock
    :param start: the start date
    :param end: the end date
    :return: a DataFrame object that contains the columns [Open, High, Low, Close, Adj Close, Volume]
    """
    df = web.DataReader(symbol, 'yahoo', start, end)
    # fill empty values
    if fill_empty:
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='backfill', inplace=True)

    return df


def get_adj_close_of_symbols(symbols, start, end, add_spy=True, fill_empty=True):
    """
    Get the adj close prices of the symbols. Add SPY by default.
    :param symbols: the symbols
    :param start: the start date
    :param end: the end date
    :param add_spy: add SPY to the symbols
    :return:
    """
    dates = pd.date_range(start, end)
    df = pd.DataFrame(index=dates)
    if add_spy and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.append('SPY')

    for symbol in symbols:
        df_temp = get_data_of_symbol(symbol, start, end, fill_empty=False)
        df_temp = df_temp['Adj Close'].to_frame()   # get the 'adj close' column and convert to DataFrame
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)

    if add_spy:  # drop dates that SPY has no trades
        df.dropna(subset=["SPY"], inplace=True)

    # fill empty values
    if fill_empty:
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='backfill', inplace=True)
    return df