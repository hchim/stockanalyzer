from Tkinter import *
from datetime import date, timedelta

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from utils.draw import plot_single_symbol
from utils.webdata import get_data_of_symbol

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
        print self.canvas.get_width_height()
        self.canvas.figure = figure
        self.canvas.draw()
        self.canvas_toolbar.update()


    def __load_figure_of_symbol(self, symbol):
        today = date.today()
        startdate = today - timedelta(days=365)

        prices = get_data_of_symbol(symbol, startdate.isoformat(), today.isoformat(), fill_empty=False)
        figure = plot_single_symbol(prices, indicators={
            # "VOLUME" : None,
            # "BB" : None,
            # "MACD" : None,
            # "SMA" : {"windows": [5, 13]},
            # "EMA" : {"windows": [5, 13]},
            # "RSI" : None,
            # "MFI" : None,
            # "CMF" : None,
            "KDJ" : {"windows": [9, 3, 3]},
            # "STOCH" : {"windows": [9, 3, 3]},
            # "ADX": {"window": 9},
            # "ATR": {"window": 14},
            # "FRAC": {"draw_breakout": True},
            # "CCI": {"window": 14},
            "OBV": None,
            "ADL": None,
        }, embed=True)

        return figure