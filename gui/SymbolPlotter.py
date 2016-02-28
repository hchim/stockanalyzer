import matplotlib.pyplot as plt
import analysis.indicators as inds
import matplotlib.patches as mpatches

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from analysis.candlestick_pattern import candlestick_patterns, fractals
from analysis.candlestick_pattern import PATTERNS

class SymbolPlotter(object):

    # indicators that should be drawn in the subfigure
    SUBFIGURE_INDICATORS = set(['macd', 'rsi', "volume", "mfi", "cmf", "kdj", "stoch", "atr", "adx", "cci", "obv",
                                   "adl"])

    def __init__(self, type="candlestick", max_candles=150, embed=False):
        """
        Parameters
        -----------
        type: string
            type of the price line, could be "candlestick" or "line"
        max_candles: int
            The maximum candlesticks to draw.
        embed: bool
            If embed is true, returns the created figure. Otherwise, invoke plt.show() to display the figure.
        """
        self.plot_type = type
        self.max_candles = max_candles
        self.embed = embed


    def __init_plotter(self):
        length = len(self.prices.index)
        if len(self.prices) > self.max_candles and self.plot_type != "line":
            self.candlestick_num = self.max_candles
        else:
            self.candlestick_num = length

        self.subfigure_num = len(self.SUBFIGURE_INDICATORS.intersection(set(self.indicators.keys())))
        self.indices = range(self.candlestick_num)

        self.figure, self.ax_array = plt.subplots(self.subfigure_num + 1, sharex=True)
        self.overlay_ax = self.ax_array    # Axes of the first subfigure
        if self.subfigure_num > 0:
            self.overlay_ax = self.ax_array[0]
        self.figure_index = 1

        # setup figure
        self.figure.tight_layout()
        self.figure.subplots_adjust(wspace=0, hspace=0.2)


    def plot_single_symbol(self, prices, indicators={}, orders=None, patterns=None):
        """
        Plot the stock prices with indicators and order signals.

        Parameters
        ----------
        prices: DataFrame
            prices of the symbols, that in clude [Open, High, Low, Close, Volume]
        indicators: dict
            It contain the indicators to draw, the values of the dict are the parameters
            of the indicator. The parameters of each indicator are shown as follows:
            BB: None
            MACD: None
            SMA: {'windows' : [5, 20, 60]}
            RSI: None (by default the window is 14) or {'window': 14}
        orders: DataFrame
            the order signals
        patterns: dict
            the candlestick patterns to draw.
        """
        self.prices = prices
        self.indicators = indicators
        self.orders = orders
        self.patterns = patterns

        self.__init_plotter()
        self.__plot_xticks()
        self.__plot_prices()
        self.__plot_indicators()

        # plot orders
        if orders is not None:
            self.__plot_orders(orders, None)

        if self.embed:
            return self.figure
        else:
            plt.show()


    def __plot_xticks(self):
        dates = self.prices.index[-self.candlestick_num:]
        span = (dates[-1] - dates[0]).days
        date_strs = [""]
        new_ind = [0]
        pre_month = dates[0].month
        pre_year = dates[0].year

        for i in self.indices:
            if dates[i].year != pre_year:
                date_strs.append(dates[i].strftime("%Y"))
                new_ind.append(i)
                pre_year = dates[i].year
                pre_month = dates[i].month
                continue

            if dates[i].month != pre_month:
                pre_month = dates[i].month
                if span > self.max_candles and dates[i].month % 3 != 1:
                    continue
                date_strs.append(dates[i].strftime("%m"))
                new_ind.append(i)

        plt.xticks(new_ind, date_strs)


    def __plot_prices(self):
        ax = self.overlay_ax
        # draw price
        if self.plot_type == "candlestick":
            self.__plot_candlestick(ax, width=0.5)
            if self.patterns is not None:
                self.__plot_candlestick_patterns(ax)
        else:
            ax.plot(self.indices, self.prices["Close"])

        ax.set_xlim([0, self.candlestick_num + 5])
        ax.grid(True)


    def __plot_indicators(self):
        # plot indicators
        for indicator in self.indicators.keys():
            params = self.indicators[indicator]
            if indicator in self.SUBFIGURE_INDICATORS:
                ax = self.ax_array[self.figure_index]
                self.figure_index += 1
            else:
                ax = self.overlay_ax

            if indicator == "volume":
                self.__plot_volume(ax, params)
            elif indicator == 'bb':
                self.__plot_bb(ax, params)
            elif indicator == "sma":
                self.__plot_sma(ax, params)
            elif indicator == "ema":
                self.__plot_ema(ax, params)
            elif indicator == 'macd':
                self.__plot_macd(ax, params)
            elif indicator == 'rsi':
                self.__plot_rsi(ax, params)
            elif indicator == "cmf":
                self.__plot_cmf(ax, params)
            elif indicator == "mfi":
                self.__plot_mfi(ax, params)
            elif indicator == 'kdj':
                self.__plot_kdj(ax, params)
            elif indicator == 'stoch':
                self.__plot_stoch(ax, params)
            elif indicator == 'adx':
                self.__plot_adx(ax, params)
            elif indicator == 'atr':
                self.__plot_atr(ax, params)
            elif indicator == 'frac':
                self.__plot_fractals(ax, params)
            elif indicator == 'cci':
                self.__plot_cci(ax, params)
            elif indicator == 'obv':
                self.__plot_obv(ax, params)
            elif indicator == 'adl':
                self.__plot_adl(ax, params)


    def __calculate_indicator(self, indicator, params):
        if params is None:
            values = getattr(inds, indicator)(self.prices)
        else:
            values = getattr(inds, indicator)(self.prices, params)
        values = values.tail(self.candlestick_num)
        return values


    def __plot_bb(self, ax, params=None):
        values = self.__calculate_indicator("bb", params)
        ax.plot(self.indices, values["Middle"], lw=0.5, color="red")
        ax.plot(self.indices, values["Upper"], lw=0.5, color="black")
        ax.plot(self.indices, values["Lower"], lw=0.5, color="black")
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)


    def __plot_macd(self, ax, params=None):
        values = self.__calculate_indicator("macd", params)

        macd_val = values["MACD"]
        for i in self.indices:
            line = Line2D(
                    xdata=(i, i), ydata=(0, macd_val[i]),
                    color = 'red' if  macd_val[i] >= 0 else 'green',
                    linewidth=1,
                    antialiased=True,
            )
            ax.add_line(line)

        ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
        ax.plot(self.indices, values["DIFF"], lw=0.5, color="red")
        ax.plot(self.indices, values["DEA"], lw=0.5, color="black")
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_orders(self, orders, params=None):
        """
        Plot order signals

        Parameters
        ----------
        orders: DataFrame
        """
        ax = self.overlay_ax
        prices = self.prices.tail(self.candlestick_num)
        dates = prices.index.tolist()
        low = prices["Low"]
        high = prices["High"]
        mean = abs(high-low).mean()

        for i in range(len(orders)):
            date = orders.loc[i, 'Date']
            operate = orders.loc[i, 'Order']
            ind = dates.index(date)
            if ind == -1:
                continue

            if operate == 'BUY':
                ax.plot(ind, low[ind] - mean, 'r^')
            else:
                ax.plot(ind, high[ind] + mean, 'gv')


    def __plot_sma(self, ax, params):
        values = self.__calculate_indicator("sma", params)
        for col in values.columns:
            ax.plot(self.indices, values[col], lw=0.5)

        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)

    def __plot_ema(self, ax, params):
        values = self.__calculate_indicator("ema", params)
        for col in values.columns:
            ax.plot(self.indices, values[col], lw=0.5)

        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)


    def __plot_rsi(self, ax, params):
        values = self.__calculate_indicator("rsi", params)

        ax.plot(self.indices, values, lw=0.5, label="RSI", color="black")
        ax.axhline(70, color="red", ls="--", alpha=0.5, lw=0.5)
        ax.axhline(30, color="green", ls="--", alpha=0.5, lw=0.5)
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.set_ylim([0, 100])
        ax.grid(b=True, axis='x')


    def __plot_cmf(self, ax, params):
        values = self.__calculate_indicator("cmf", params)

        ax.plot(self.indices, values, lw=0.5, label="CMF", color="black")
        ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_mfi(self, ax, params=None):
        values = self.__calculate_indicator("mfi", params)

        ax.plot(self.indices, values, lw=0.5, label="MFI", color="black")
        ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
        ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
        ax.set_ylim([0, 100])
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_kdj(self, ax, params):
        values = self.__calculate_indicator("kdj", params)

        ax.plot(self.indices, values["K"], lw=0.5, color="red")
        ax.plot(self.indices, values["D"], lw=0.5, color="black")
        ax.plot(self.indices, values["J"], lw=0.5, color="blue")
        ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
        ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_stoch(self, ax, params):
        values = self.__calculate_indicator("stoch", params)

        ax.plot(self.indices, values["K"], color="red", lw=0.5)
        ax.plot(self.indices, values["D"], color="black", lw=0.5)
        ax.axhline(80, color="red", ls="--", alpha=0.5, lw=0.5)
        ax.axhline(50, color="black", ls="--", alpha=0.5, lw=0.5)
        ax.axhline(20, color="green", ls="--", alpha=0.5, lw=0.5)
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_volume(self, ax, params=None):
        if params is None:
            width = 0.6
        else:
            width = params["width"]
        prices = self.prices.tail(self.candlestick_num)

        for i in self.indices:
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
        ax.grid(b=True, axis='x')


    def __plot_candlestick(self, ax, width=0.5, colorup='red', colordown='green', alpha=0.8):
        offset = width / 2.0
        line_width = width * 2
        prices = self.prices.tail(self.candlestick_num)

        for i in self.indices:
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


    def __plot_candlestick_patterns(self, ax, patterns, candle_width=0.5):
        pattern_signals = candlestick_patterns(self.prices, patterns).tail(self.candlestick_num)
        prices = self.prices.tail(self.candlestick_num)

        offset = candle_width/2
        for i in self.indices:
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


    def __plot_adx(self, ax, params):
        values = self.__calculate_indicator("adx", params)
        pdi = values["+DI"]
        mdi = values["-DI"]
        adx_val = values["ADX"]

        ax.plot(self.indices, adx_val, color='black')
        ax.plot(self.indices, pdi, lw=0.5, color='red')
        ax.plot(self.indices, mdi, lw=0.5, color='green')
        ax.axhline(25, color="blue", ls="--", alpha=0.5, lw=0.5)
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_atr(self, ax, params):
        values = self.__calculate_indicator("atr", params)

        ax.plot(self.indices, values, lw=0.5, color='black', label="ATR")
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_fractals(self, ax, params={"draw_breakout": True}):
        frac, breakout = fractals(self.prices)
        frac = frac.tail(self.candlestick_num)
        breakout = breakout.tail(self.candlestick_num)
        prices = self.prices.tail(self.candlestick_num)

        high = prices["High"]
        low = prices["Low"]
        mean = abs(high-low).mean()

        pre_up = -1
        pre_down = -1
        for i in self.indices:
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


    def __plot_cci(self, ax, params={"window": 20}):
        values = self.__calculate_indicator("cci", params)
        cci_val = values["CCI"]

        ax.plot(self.indices, cci_val, lw=0.5, color='black', label="CCI")
        ax.fill_between(self.indices, 100, cci_val, where=cci_val>=100, facecolor='red', alpha=0.3, interpolate=True)
        ax.fill_between(self.indices, -100, cci_val, where=cci_val<=-100, facecolor='green', alpha=0.3, interpolate=True)
        ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
        ax.axhline(100, color="green", lw=0.5)
        ax.axhline(-100, color="red", lw=0.5)
        ax.axhline(200, color="green", lw=0.5, ls='--')
        ax.axhline(-200, color="red", lw=0.5, ls='--')
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')


    def __plot_obv(self, ax, params=None):
        values = self.__calculate_indicator("obv", params)
        obv_val = values["OBV"]

        ax.plot(self.indices, obv_val, lw=0.5, color='blue', label="OBV")
        ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')
        ax.grid(b=True, axis='y')


    def __plot_adl(self, ax, params=None):
        values = self.__calculate_indicator("adl", params)
        adl_val = values["ADL"]

        ax.plot(self.indices, adl_val, lw=0.5, color='blue', label="ADL")
        ax.axhline(0, color="black", ls="--", alpha=0.5, lw=0.5)
        ax.legend(loc=2, ncol=3, frameon=False, fontsize="small", framealpha=0.5)
        ax.grid(b=True, axis='x')
        ax.grid(b=True, axis='y')