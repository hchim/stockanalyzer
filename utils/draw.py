import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from analysis.indicators import sma, bollinger_bands, ema, macd, rsi, mfi, cmf, kdj, stoch, adx, atr
from analysis.candlestick_pattern import candlestick_patterns
from analysis.candlestick_pattern import PATTERNS


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


def plot_single_symbol(prices, type="candlestick", indicators={}, orders=None, patterns=None):
    """
    Plot the stock prices with indicators and order signals.

    Parameters
    ----------
    prices: DataFrame
        prices of the symbols, that in clude [Open, High, Low, Close, Volume]
    type: string
        type of the price line, could be "candlestick" or "line"
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

    subfigure_indicator_set = set(['MACD', 'RSI', "VOLUME", "MFI", "CMF", "KDJ", "STOCH", "ATR", "ADX"]) # the set of indicators that must be draw in a subfigure
    subfigure_number = len(subfigure_indicator_set.intersection(set(indicators.keys())))
    figure, axarr = plt.subplots(subfigure_number + 1, sharex=True)
    ax = axarr    # Axes of the first subfigure
    if subfigure_number > 0:
        ax = axarr[0]
    figure_index = 1
    indices = range(len(prices))

    # setup figure
    figure.tight_layout()
    figure.subplots_adjust(wspace=0, hspace=0.2)
    plot_xticks(prices.index, indices)

    # draw price
    if type == "candlestick":
        plot_candlestick(ax, prices, width=0.5)
        if patterns is not None:
            plot_candlestick_patterns(ax, prices, patterns)
    else:
        ax.plot(range(len(prices)), close_prices)

    ax.set_ylabel("Price")
    ax.set_xlim([0, len(close_prices) + 5])
    ax.grid(True)

    # plot indicators
    for indicator in indicators.keys():
        params = indicators[indicator]
        if indicator == "VOLUME":
            plot_volume(axarr[figure_index], prices)
            figure_index += 1
        elif indicator == 'BB':
            plot_bollinger_band(ax, close_prices)
        elif indicator.startswith("SMA"):
            window = int(indicator[3:])
            plot_sma(ax, close_prices, window)
        elif indicator.startswith("EMA"):
            window = int(indicator[3:])
            plot_ema(ax, close_prices, window)
        elif indicator == 'MACD':
            plot_macd(axarr[figure_index], close_prices)
            figure_index += 1
        elif indicator == 'RSI':
            plot_rsi(axarr[figure_index], close_prices, params)
            figure_index += 1
        elif indicator == "CMF":
            plot_cmf(axarr[figure_index], prices)
            figure_index += 1
        elif indicator == "MFI":
            plot_mfi(axarr[figure_index], prices)
            figure_index += 1
        elif indicator == 'KDJ':
            plot_kdj(axarr[figure_index], prices, params)
            figure_index += 1
        elif indicator == 'STOCH':
            plot_stoch(axarr[figure_index], prices, params)
            figure_index += 1
        elif indicator == 'ADX':
            plot_adx(axarr[figure_index], prices, params)
            figure_index += 1
        elif indicator == 'ATR':
            plot_atr(axarr[figure_index], prices, params)
            figure_index += 1

    # plot orders
    if orders is not None:
        plot_orders(ax, orders, prices)

    plt.show()


def plot_xticks(dates, indices):
    date_strs = [""]
    new_ind = [0]
    pre_month = dates[0].month
    for i in indices:
        if dates[i].month != pre_month:
            date_strs.append(dates[i].strftime("%b"))
            new_ind.append(i)
            pre_month = dates[i].month
    plt.xticks(new_ind, date_strs)


def plot_bollinger_band(ax, prices):
    middle, upper, lower = bollinger_bands(prices)
    indices = range(len(prices))
    ax.plot(indices, middle, lw=0.5)
    ax.plot(indices, upper, lw=0.5)
    ax.plot(indices, lower, lw=0.5)


def plot_macd(ax, prices):
    macd_val, signal, histogram = macd(prices)
    indices = range(len(prices))
    for i in indices:
        line = Line2D(
            xdata=(i, i), ydata=(0, histogram.ix[i]),
            color = 'red',
            linewidth=1,
            antialiased=True,
        )
        ax.add_line(line)

    ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
    ax.plot(indices, macd_val, lw=0.5)
    ax.plot(indices, signal, lw=0.5)
    ax.set_ylabel('MACD')
    ax.grid(b=True, axis='x')

def plot_orders(ax, orders, prices):
    """
    Plot order signals

    Parameters
    ----------
    ax: Axes
    orders: DataFrame
    prices: DataFrame
    """
    dates = prices.index.tolist()
    for i in range(len(orders)):
        date = orders.loc[i, 'Date']
        operate = orders.loc[i, 'Order']
        ind = dates.index(date)

        if operate == 'BUY':
            price = prices.loc[date, 'Low']
            ax.plot(ind, price, '^', color='green')
        else:
            price = prices.loc[date, 'High']
            ax.plot(ind, price, 'v', color='red')


def plot_sma(ax, prices, window):
    sma_val = sma(prices, window)
    ax.plot(range(len(sma_val)), sma_val, lw=0.5)


def plot_ema(ax, prices, window):
    ema_val = ema(prices, window)
    ax.plot(range(len(ema_val)), ema_val, lw=0.5)


def plot_rsi(ax, prices, params):
    if not params:
        window = 14
    else:
        window = params['window']

    rsi_val = rsi(prices, window)
    ax.plot(range(len(rsi_val)), rsi_val, lw=0.5)
    ax.axhline(70, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(30, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('RSI')
    ax.set_ylim([0, 100])
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def plot_cmf(ax, prices):
    cmf_val = cmf(prices)

    ax.plot(range(len(cmf_val)), cmf_val, lw=0.5)
    ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('CMF')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def plot_mfi(ax, prices):
    mfi_val = mfi(prices)

    ax.plot(range(len(mfi_val)), mfi_val, lw=0.5)
    ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylim([0, 100])
    ax.set_ylabel('MFI')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def plot_kdj(ax, prices, params):
    kdj_val = kdj(prices, params)
    indices = range(len(kdj_val))
    ax.plot(indices, kdj_val, lw=0.5)
    ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('KDJ')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def plot_stoch(ax, prices, params):
    kd_val = stoch(prices, params)
    indices = range(len(kd_val))
    ax.plot(indices, kd_val, lw=0.5)
    ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(50, color="black", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('STOCH')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def plot_volume(ax, prices, width=0.6):
    for i in range(len(prices)):
        p = prices.iloc[i, :]
        open = p["Open"]
        close = p["Close"]
        volume = p["Volume"]

        if close >= open:
            color = "red"
        else:
            color = "green"

        rect = Rectangle(
            xy = (i - width/2, 0),
            width = width,
            height = volume,
            facecolor = color,
            edgecolor = color,
        )
        rect.set_alpha(0.5)
        ax.add_patch(rect)
    ax.set_ylim([0, prices["Volume"].max() * 1.25])
    ax.set_ylabel('Volume')
    ax.grid(b=True, axis='x')


def plot_histogram(data, bins=20):
    data.hist(bins=bins)
    plt.show()


def plot_scatter(data, beta, alpha, y_symbol, x_symbol = "SPY"):
    data.plot(kind='scatter', x=x_symbol, y=y_symbol) # draw scatter figure
    plt.plot(data[x_symbol], beta*data[x_symbol] + alpha, '-', color='r')
    plt.show()


def plot_candlestick(ax, prices, width=0.5, colorup='red', colordown='green', alpha=0.8):
    offset = width / 2.0
    line_width = width * 2

    for i in range(len(prices.index)):
        p = prices.iloc[i, :]
        open = p["Open"]
        close = p["Close"]
        high = p["High"]
        low = p["Low"]

        box_high = max(open, close)
        box_low = min(open, close)
        height = box_high - box_low

        if close >= open:
            color = colorup
        else:
            color = colordown

        vline_low = Line2D(
            xdata=(i, i), ydata=(low, box_low),
            color = 'black',
            linewidth=line_width,
            antialiased=True,
        )

        vline_high = Line2D(
            xdata=(i, i), ydata=(box_high, high),
            color = 'black',
            linewidth=line_width,
            antialiased=True,
        )

        rect = Rectangle(
            xy = (i - offset, box_low),
            width = width,
            height = height,
            facecolor = color,
            edgecolor = color,
        )

        rect.set_alpha(alpha)
        ax.add_line(vline_low)
        ax.add_line(vline_high)
        ax.add_patch(rect)

    ax.autoscale_view()


def plot_candlestick_patterns(ax, prices, patterns, candle_width=0.5):
    pattern_signals = candlestick_patterns(prices, patterns)
    offset = candle_width/2
    for i in range(len(prices.index)):
        for j in range(len(patterns)):
            val = pattern_signals.iloc[i, j]
            if val == 0:
                continue

            pattern = PATTERNS[patterns[j]]
            if val < 0:
                color = "green"
            else:
                color = "red"

            start_ind = i - pattern["candles"] + 1
            included_prices = prices.iloc[start_ind:i+1, :]
            max = included_prices["High"].max()
            min = included_prices["Low"].min()
            rect = Rectangle(
                xy = (start_ind - offset, min),
                width = pattern["candles"],
                height = max - min,
                fill=False,
                edgecolor=color
            )

            # TODO Add pattern name
            # ax.annotate(pattern["name"], res.xy, ,)

            ax.add_patch(rect)


def plot_adx(ax, prices, params):
    adx_val, pdi, mdi = adx(prices, params)
    indices = range(len(adx_val))
    ax.plot(indices, adx_val, lw=0.5, color='black')
    ax.plot(indices, pdi, lw=0.5, color='green')
    ax.plot(indices, mdi, lw=0.5, color='red')
    ax.axhline(25, color="blue", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('ADX')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def plot_atr(ax, prices, params):
    atr_val = atr(prices, params)
    indices = range(len(atr_val))
    ax.plot(indices, atr_val, lw=0.5, color='black')
    ax.set_ylabel('ATR')
    ax.legend_ = None
    ax.grid(b=True, axis='x')