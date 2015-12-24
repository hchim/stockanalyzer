import matplotlib.pyplot as plt
import pandas as pd

from analysis.indicators import sma, bollinger_bands, ema, macd


def normalize_data(df):
    return df/df.iloc[0]

def plot_multi_symbols(prices, title="Stock Prices", xlabel="Date", ylabel="Price", normalize=False):
    """
    Plot multiple symbols

    Parameters
    ----------
    prices: DataFrame
        prices of the symbols
    title: string
        the title of the figure
    xlabel: string
        the x axis of the figure
    ylabel: string
        the y axis of the figure
    normalize: boolean
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

    Parameters
    ----------
    prices: DataFrame
        prices of the symbols
    title: string
        the title of the figure
    xlabel: string
        the x axis of the figure
    ylabel: string
        the y axis of the figure
    indicators: dict
        It contain the indicators to draw, the values of the dict are the parameters
        of the indicator. The indicator can be:
        BB:
        MACD:
        SMA:
    orders: DataFrame
        the order signals
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
    middle, upper, lower = bollinger_bands(prices)
    middle.plot(label='Rolling mean', ax=ax)
    upper.plot(label='Upper band', ax=ax)
    lower.plot(label='Lower band', ax=ax)


def plot_macd(ax, prices):
    macd_val, signal, histogram = macd(prices)

    ax.fill_between(histogram.index, 0, histogram, alpha=0.5)
    macd_val.plot(label='MACD', ax=ax)
    signal.plot(label='Signal', ax=ax)


def plot_orders(ax, orders, prices):
    """
    Plot order signals

    Parameters
    ----------
    ax: Axes
    orders: DataFrame
    prices: DataFrame
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
    for window in windows:
        sma_val = sma(prices, window)
        sma_val.plot(label="SMA{}".format(window), ax=ax)