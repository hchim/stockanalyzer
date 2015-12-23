import matplotlib.pyplot as plt
import pandas as pd

from analysis.indicators import sma, bollinger_bands, ema, macd


def normalize_data(df):
    """
    Normalize the values in the DataFrame.
    :param df: the DataFrame
    :return:
    """
    return df/df.iloc[0]

def plot_multi_symbols(prices, title="Stock Prices", xlabel="Date", ylabel="Price", normalize=False):
    """
    Plot multiple symbols
    :param prices: prices of the symbols
    :param title: the title of the figure
    :param xlabel: the x axis of the figure
    :param ylabel: the y axis of the figure
    """
    if normalize:
        prices = normalize_data(prices)

    ax = prices.plot(title=title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.show()


def plot_single_symbol(prices, title="Stock Prices", xlabel="Date", ylabel="Price", indicators={}, orders=None):
    """
    Plot the stock prices with indicators and order signals.
    :param prices: prices of the symbols
    :param title: the title of the figure
    :param xlabel: the x axis of the figure
    :param ylabel: the y axis of the figure
    :param indicators: a map object that contain the indicators to draw, the values of the map are the parameters
                       of the indicator. The indicator can be:
                       BB:
                       MACD:
                       SMA:
    :param orders: DataFrame object that contain the order signals
    """
    if isinstance(prices, pd.DataFrame):
        prices = prices['Adj Close']

    subfigure_indicator_set = set(['MACD']) # the set of indicators that must be draw in a subfigure
    subfigure_number = len(subfigure_indicator_set.intersection(set(indicators.keys())))
    figure, axarr = plt.subplots(subfigure_number + 1, sharex=True)
    ax = axarr    # Axes of the first subfigure
    if subfigure_number > 0:
        ax = axarr[0]
    figure_index = 1

    # setup figure
    figure.subplots_adjust(hspace=0)

    # draw price
    prices.plot(label="Price", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # plot indicators
    for indicator in indicators.keys():
        if indicator == 'BB':
            plot_bollinger_band(ax, prices)
        elif indicator == 'SMA':
            plot_sma(ax, prices, indicators[indicator])
        elif indicator == 'MACD':
            plot_macd(axarr[figure_index], prices)
            figure_index += 1

    # plot orders
    if orders is not None:
        plot_orders(ax, orders, prices)

    plt.show()


def plot_bollinger_band(ax, prices):
    """
    Plot bollinger band
    :param ax: the Axes to draw
    :param prices: the prices of the symbol
    """
    middle, upper, lower = bollinger_bands(prices)
    middle.plot(label='Rolling mean', ax=ax)
    upper.plot(label='Upper band', ax=ax)
    lower.plot(label='Lower band', ax=ax)


def plot_macd(ax, prices):
    """
    Plot macd
    :param ax: the Axes to draw
    :param prices: the prices of the symbol
    """
    macd_val, signal, histogram = macd(prices)
    #    ax.hist(histgram.iloc[:, 0], len(histgram.index))
    #    histgram.plot(ax=ax)
    macd_val.plot(label='MACD', ax=ax)
    signal.plot(label='Signal', ax=ax)


def plot_orders(ax, orders, prices):
    """
    Plot order signals
    :param ax:
    :param orders:
    :param prices:
    """
    for i in range(len(orders)):
        date = orders.loc[i, 'Date']
        operate = orders.loc[i, 'Order']
        price = prices.loc[date]

        if operate == 'BUY':
            ax.plot(date, price, '^', color='green')
        else:
            ax.plot(date, price, 'v', color='red')


def plot_sma(ax, prices, windows):
    """
    Plot moving averages
    :param ax: the Axes to draw
    :param prices: the prices of the stock
    :param window: the array of the windows
    """
    for window in windows:
        sma_val = sma(prices, window)
        sma_val.plot(label="SMA{}".format(window), ax=ax)