import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from analysis.indicators import sma, bollinger_bands, ema, macd, rsi, mfi, cmf, kdj, stoch, adx, atr, cci
from analysis.candlestick_pattern import candlestick_patterns, fractals
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


def plot_scatter(data, beta, alpha, y_symbol, x_symbol = "SPY"):
    data.plot(kind='scatter', x=x_symbol, y=y_symbol) # draw scatter figure
    plt.plot(data[x_symbol], beta*data[x_symbol] + alpha, '-', color='r')
    plt.show()

def plot_histogram(data, bins=20):
    data.hist(bins=bins)
    plt.show()


def plot_single_symbol(prices, type="candlestick", indicators={}, orders=None, patterns=None, embed=False):
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
    embed: bool
        If embed is true, returns the created figure. Otherwise, invoke plt.show() to display the figure.
    """

    close_prices = prices['Close']
    # the set of indicators that must be draw in a subfigure
    subfigure_indicator_set = set(['MACD', 'RSI', "VOLUME", "MFI", "CMF", "KDJ", "STOCH", "ATR", "ADX", "CCI"])
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
    __plot_xticks(prices.index, indices)

    # draw price
    if type == "candlestick":
        __plot_candlestick(ax, prices, width=0.5)
        if patterns is not None:
            __plot_candlestick_patterns(ax, prices, patterns)
    else:
        ax.plot(range(len(prices)), close_prices)

    ax.set_ylabel("Price")
    ax.set_xlim([0, len(close_prices) + 5])
    ax.grid(True)

    # plot indicators
    for indicator in indicators.keys():
        params = indicators[indicator]
        if indicator == "VOLUME":
            __plot_volume(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == 'BB':
            __plot_bollinger_band(ax, indices, prices, params)
        elif indicator == "SMA":
            __plot_sma(ax, indices, prices, params)
        elif indicator == "EMA":
            __plot_ema(ax, indices, prices, params)
        elif indicator == 'MACD':
            __plot_macd(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == 'RSI':
            __plot_rsi(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == "CMF":
            __plot_cmf(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == "MFI":
            __plot_mfi(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == 'KDJ':
            __plot_kdj(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == 'STOCH':
            __plot_stoch(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == 'ADX':
            __plot_adx(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == 'ATR':
            __plot_atr(axarr[figure_index], indices, prices, params)
            figure_index += 1
        elif indicator == 'FRAC':
            __plot_fractals(ax, indices, prices, params)
        elif indicator == 'CCI':
            __plot_cci(axarr[figure_index], indices, prices, params)
            figure_index += 1

    # plot orders
    if orders is not None:
        __plot_orders(ax, indices, orders, prices, params)

    if embed:
        return figure
    else:
        plt.show()


def __plot_xticks(dates, indices):
    date_strs = [""]
    new_ind = [0]
    pre_month = dates[0].month
    for i in indices:
        if dates[i].month != pre_month:
            date_strs.append(dates[i].strftime("%b"))
            new_ind.append(i)
            pre_month = dates[i].month
    plt.xticks(new_ind, date_strs)


def __plot_bollinger_band(ax, indices, prices, params=None):
    if params is None:
        values = bollinger_bands(prices)
    else:
        values = bollinger_bands(prices, params)

    ax.plot(indices, values, lw=0.5)


def __plot_macd(ax, indices, prices, params=None):
    if params is None:
        values = macd(prices)
    else:
        values = macd(prices, params)

    macd_val = values["MACD"]
    for i in indices:
        line = Line2D(
            xdata=(i, i), ydata=(0, macd_val[i]),
            color = 'red' if  macd_val[i] >= 0 else 'green',
            linewidth=1,
            antialiased=True,
        )
        ax.add_line(line)

    ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
    ax.plot(indices, values, lw=0.5)
    ax.set_ylabel('MACD')
    ax.grid(b=True, axis='x')


def __plot_orders(ax, indices, orders, prices, params):
    """
    Plot order signals

    Parameters
    ----------
    ax: Axes
    indices: array
    orders: DataFrame
    prices: DataFrame
    """
    dates = prices.index.tolist()
    low = prices["Low"]
    high = prices["High"]
    mean = abs(high-low).mean()

    for i in range(len(orders)):
        date = orders.loc[i, 'Date']
        operate = orders.loc[i, 'Order']
        ind = dates.index(date)

        if operate == 'BUY':
            ax.plot(ind, low[ind] - mean, 'r^')
        else:
            ax.plot(ind, high[ind] + mean, 'gv')


def __plot_sma(ax, indices, prices, params):
    sma_val = sma(prices, params)
    ax.plot(indices, sma_val, lw=0.5)


def __plot_ema(ax, indices, prices, params):
    ema_val = ema(prices, params=params)
    ax.plot(indices, ema_val, lw=0.5)


def __plot_rsi(ax, indices, prices, params):
    if params is None:
        rsi_val = rsi(prices)
    else:
        rsi_val = rsi(prices, params)

    ax.plot(indices, rsi_val, lw=0.5)
    ax.axhline(70, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(30, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('RSI')
    ax.set_ylim([0, 100])
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def __plot_cmf(ax, indices, prices, params):
    if params is None:
        cmf_val = cmf(prices)
    else:
        cmf_val = cmf(prices, params)

    ax.plot(indices, cmf_val, lw=0.5)
    ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('CMF')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def __plot_mfi(ax, indices, prices, params=None):
    if params is None:
        mfi_val = mfi(prices)
    else:
        mfi_val = mfi(prices, params)

    ax.plot(indices, mfi_val, lw=0.5)
    ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylim([0, 100])
    ax.set_ylabel('MFI')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def __plot_kdj(ax, indices, prices, params):
    kdj_val = kdj(prices, params)

    ax.plot(indices, kdj_val, lw=0.5)
    ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('KDJ')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def __plot_stoch(ax, indices, prices, params):
    kd_val = stoch(prices, params)

    ax.plot(indices, kd_val, lw=0.5)
    ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(50, color="black", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('STOCH')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def __plot_volume(ax, indices, prices, params=None):
    if params is None:
        width = 0.6
    else:
        width = params["width"]

    for i in indices:
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


def __plot_candlestick(ax, prices, width=0.5, colorup='red', colordown='green', alpha=0.8):
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


def __plot_candlestick_patterns(ax, prices, patterns, candle_width=0.5):
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


def __plot_adx(ax, indices, prices, params):
    adx_val = adx(prices, params)
    pdi = adx_val["+DI"]
    mdi = adx_val["-DI"]
    adx_val = adx_val["ADX"]

    ax.plot(indices, adx_val, color='black')
    ax.plot(indices, pdi, lw=0.5, color='red')
    ax.plot(indices, mdi, lw=0.5, color='green')
    ax.axhline(25, color="blue", ls="--", alpha=0.5, lw=0.5)
    ax.set_ylabel('ADX')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def __plot_atr(ax, indices, prices, params):
    atr_val = atr(prices, params)

    ax.plot(indices, atr_val, lw=0.5, color='black')
    ax.set_ylabel('ATR')
    ax.legend_ = None
    ax.grid(b=True, axis='x')


def __plot_fractals(ax, indices, prices, params={"draw_breakout": True}):
    frac, breakout = fractals(prices)
    high = prices["High"]
    low = prices["Low"]
    mean = abs(high-low).mean()

    pre_up = -1
    pre_down = -1
    for i in indices:
        # check breakout
        if params["draw_breakout"]:
            if breakout[i] == 1:
                ax.plot([pre_up, i], [high[pre_up], high[pre_up]], color="red")
            elif breakout[i] == -1:
                ax.plot([pre_down, i], [low[pre_down], low[pre_down]], color="green")
        # draw fractals
        if frac[i] == 1:
            ax.plot(i, high[i] + mean, 'r^')
            pre_up = i
        elif frac[i] == -1:
            ax.plot(i, low[i] - mean, 'gv')
            pre_down = i


def __plot_cci(ax, indices, prices, params={"window": 20}):
    cci_val = cci(prices, params)
    cci_val = cci_val["CCI"]

    ax.plot(indices, cci_val, lw=0.5, color='black')
    ax.fill_between(indices, 100, cci_val, where=cci_val>=100, facecolor='red', alpha=0.3, interpolate=True)
    ax.fill_between(indices, -100, cci_val, where=cci_val<=-100, facecolor='green', alpha=0.3, interpolate=True)
    ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
    ax.axhline(100, color="green", lw=0.5)
    ax.axhline(-100, color="red", lw=0.5)
    ax.axhline(200, color="green", lw=0.5, ls='--')
    ax.axhline(-200, color="red", lw=0.5, ls='--')
    ax.set_ylabel('CCI')
    ax.legend_ = None
    ax.grid(b=True, axis='x')