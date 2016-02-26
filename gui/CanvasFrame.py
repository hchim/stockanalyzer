from Tkinter import *
from datetime import date, timedelta

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from gui.SymbolPlotter import SymbolPlotter
from utils.webdata import get_data_of_symbol
from analysis.basic import daily_prices_to_weekly_prices

class CanvasFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)


    def init_canvas(self, symbol):
        figure = self.__load_figure_of_symbol(symbol)
        canvas = FigureCanvasTkAgg(figure, self)
        self.canvas = canvas
        canvas.show()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        self.canvas_toolbar = toolbar
        toolbar.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=True)


    def update_figure(self, symbol):
        figure = self.__load_figure_of_symbol(symbol)
        self.canvas.figure = figure
        self.canvas.draw()
        self.canvas_toolbar.update()


    def __load_figure_of_symbol(self, symbol):
        today = date.today()
        startdate = today - timedelta(days=3650)

        prices = get_data_of_symbol(symbol, startdate.isoformat(), today.isoformat(), fill_empty=False)
        prices = daily_prices_to_weekly_prices(prices)
        plotter = SymbolPlotter(embed=True)
        figure = plotter.plot_single_symbol(prices, indicators={
            # "VOLUME" : None,
            # "BB" : None,
            # "MACD" : None,
            # "SMA" : {"windows": [5, 13]},
            # "EMA" : {"windows": [5, 13]},
            # "RSI" : None,
            # "MFI" : None,
            # "CMF" : None,
            # "KDJ" : {"windows": [9, 3, 3]},
            "STOCH" : {"windows": [9, 3, 3]},
            "ADX": {"window": 14},
            # "ATR": {"window": 14},
            # "FRAC": {"draw_breakout": True},
            "CCI": {"window": 14},
            # "OBV": None,
            # "ADL": None,
        })

        return figure