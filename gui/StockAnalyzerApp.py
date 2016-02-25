import matplotlib
matplotlib.use("TkAgg")
import Tkinter as tk
import tkMessageBox as msgbox
import sys

from gui.CanvasFrame import CanvasFrame


class StockAnalyzerApp():

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Analyzer")

        self.__init_menubar()

        # protocols
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=8)
        self.root.grid_columnconfigure(1, weight=1)

        self.canvas_panel = CanvasFrame(self.root)
        self.canvas_panel.grid(row=0, column=0, sticky="nsew")
        self.canvas_panel.init_canvas("SPY")

        self.symbol_panel = tk.Frame(self.root)
        self.symbol_panel.grid(row=0, column=1, sticky="nsew")
        self.__init_symbol_panel()


    def __init_symbol_panel(self):
        symbol_list = tk.Listbox(self.symbol_panel, selectmode=tk.SINGLE)
        symbol_list.pack(fill=tk.BOTH, expand=True)
        symbol_list.bind('<<ListboxSelect>>', self.__on_symbol_selected)

        symbols = [{"symbol":"AAPL"}, {"symbol":"AMZN"}]
        for symbol in symbols:
            symbol_list.insert(tk.END, symbol["symbol"])


    def __on_symbol_selected(self, event):
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        self.canvas_panel.update_figure(value)


    def __init_menubar(self):
        menubar = tk.Menu(self.root)
        #File Menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=menubar)


    def quit(self):
        self.root.quit()
        self.root.destroy()
        sys.exit()


    def run(self):
        self.root.mainloop()