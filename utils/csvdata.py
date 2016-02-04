import pandas as pd
import os

def get_data_of_symbol(symbol, start, end, fill_empty=True):
    """
    Get the daily prices of the symbol in the specified range from csv file.

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
    csvfile = "data/prices/{}.csv".format(symbol)
    dates = pd.date_range(start, end)
    df = pd.DataFrame(index=dates)
    dateparser = lambda x: pd.datetime.strptime(x, '%d-%b-%y')
    df_temp = pd.read_csv(csvfile, index_col=0, parse_dates=[0], date_parser=dateparser,  na_values=['nan', '-'])
    df = df.join(df_temp)
    df.dropna(inplace=True)

    # fill empty values
    if fill_empty:
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='backfill', inplace=True)

    return df

def get_available_symbols():
    """
    Get the symbols in the data/prices/ directory.
    """
    symbols = []
    for file in os.listdir("data/prices/"):
        if file.endswith(".csv"):
            symbols.append(file[:-4])

    return symbols