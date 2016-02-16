import Tkinter as tk
import gui.Theme as theme

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from utils.draw import plot_single_symbol
from utils.webdata import get_data_of_symbol


class HomeFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # TODO set these values based on gui
        startdate = '2015-08-01'
        enddate = '2016-02-15'
        prices = get_data_of_symbol('JMEI', startdate, enddate, fill_empty=False)
        figure = plot_single_symbol(prices, indicators={
            # "VOLUME" : None,
            # "BB" : None,
            # "MACD" : None,
            # "SMA" : {"windows": [5, 13]},
            # "EMA" : {"windows": [5, 13]},
            # "RSI" : None,
            # "MFI" : None,
            # "CMF" : None,
            # "KDJ" : {"windows": [9, 3, 3]},
            # "STOCH" : {"windows": [9, 3, 3]},
            "ADX": {"window": 9},
            "ATR": {"window": 14},
            # "FRAC": {"draw_breakout": True},
            "CCI": {"window": 14},
        }, embed=True)

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)