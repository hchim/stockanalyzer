import matplotlib
matplotlib.use("TkAgg")
import Tkinter as tk
import tkMessageBox as msgbox
import sys

from gui.HomeFrame import HomeFrame


class StockAnalyzerApp():

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Analyzer")

        self.__init_menubar()

        # protocols
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.container = tk.Frame(self.root)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        home_frame = HomeFrame(self.container)
        home_frame.grid(row=0, column=0, sticky="nsew")
        home_frame.tkraise()


    def __init_menubar(self):
        menubar = tk.Menu(self.root)
        #File Menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=menubar)


    def quit(self, quiet=False):
        if quiet is False:
            if msgbox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()
                sys.exit()


    def run(self):
        self.root.mainloop()