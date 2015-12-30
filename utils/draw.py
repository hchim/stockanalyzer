import matplotlib.pyplot as plt
import pandas as pd

from analysis.indicators import sma, bollinger_bands, ema, macd, rsi


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
        prices of the symbols, that in clude [Open, High, Low, Close, Volume]
    title: string
        the title of the figure
    xlabel: string
        the x axis of the figure
    ylabel: string
        the y axis of the figure
    indicators: dict
        It contain the indicators to draw, the values of the dict are the parameters
        of the indicator. The parameters of each indicator are shown as follows:
        BB: None
        MACD: None
        SMA: {'windows' : [5, 20, 60]}
        RSI: None (by default the window is 14) or {'window': 14}
    orders: DataFrame
        the order signals
    """

    close_prices = prices['Close']

    subfigure_indicator_set = set(['MACD', 'RSI', "VOLUME"]) # the set of indicators that must be draw in a subfigure
    subfigure_number = len(subfigure_indicator_set.intersection(set(indicators.keys())))
    figure, axarr = plt.subplots(subfigure_number + 1, sharex=True)
    ax = axarr    # Axes of the first subfigure
    if subfigure_number > 0:
        ax = axarr[0]
    figure_index = 1

    # setup figure

    # draw price
    close_prices.plot(label="Price", ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # plot indicators
    for indicator in indicators.keys():
        if indicator == "VOLUME":
            volumes = prices['Volume'] * prices['Close']
            plot_volume(axarr[figure_index], volumes)
            figure_index += 1
        elif indicator == 'BB':
            plot_bollinger_band(ax, close_prices)
        elif indicator == 'SMA':
            plot_sma(ax, close_prices, indicators[indicator])
        elif indicator == 'MACD':
            plot_macd(axarr[figure_index], close_prices)
            figure_index += 1
        elif indicator == 'RSI':
            plot_rsi(axarr[figure_index], close_prices, indicators[indicator])
            figure_index += 1

    # plot orders
    if orders is not None:
        plot_orders(ax, orders, close_prices)

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
    ax.set_ylabel('MACD')

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


def plot_sma(ax, prices, params):
    for window in params['windows']:
        sma_val = sma(prices, window)
        sma_val.plot(label="SMA{}".format(window), ax=ax)


def plot_rsi(ax, prices, params):
    if not params:
        window = 14
    else:
        window = params['windows']

    rsi_val = rsi(prices, window)

    rsi_val.plot(label='RSI', ax=ax)
    ax.axhline(70, color="red")
    ax.axhline(30, color="green")
    ax.set_ylabel('RSI')


def plot_volume(ax, volums):
    volums.plot(label="Volume", ax=ax)
    ax.set_ylabel('Volume')


def plot_histogram(data, bins=20):
    data.hist(bins=bins)
    plt.show()


def plot_scatter(data, beta, alpha, y_symbol, x_symbol = "SPY"):
    data.plot(kind='scatter', x=x_symbol, y=y_symbol) # draw scatter figure
    plt.plot(data[x_symbol], beta*data[x_symbol] + alpha, '-', color='r')
    plt.show()