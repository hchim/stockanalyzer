from analysis.candlestick_pattern import candlestick_patterns, GOOD_PATTERNS
from utils.webdata import get_data_of_symbol
from datetime import date, timedelta

import csv

"""
Analyze the candlestick patterns of NYSE and NASDAQ symbols (price > 0 and marketcap > 1B) in the last trading day.
"""
class PatternAnalyzer(object):

    def __init__(self, symbols, outfile):
        self.symbols = symbols
        self.outfile = outfile


    def analyze(self):
        csvfile = open(self.outfile, 'wb')
        self.writer = csv.writer(csvfile, delimiter=',')

        for symbol in self.symbols:
            self.__analyze_pattern(symbol)


    def __analyze_pattern(self, symbol):
        enddate = date.today()
        startdate = enddate - timedelta(30)

        prices = get_data_of_symbol(symbol, startdate, enddate, fill_empty=False)
        if prices is None:
            return

        prices.dropna(how="any")
        if len(prices.index) == 0:
            return

        patterns = candlestick_patterns(prices, GOOD_PATTERNS)
        self.__print_lastday_pattern(patterns.iloc[-1, :], symbol)


    def __print_lastday_pattern(self, patterns, symbol):
        for col in GOOD_PATTERNS:
            if patterns[col] != 0:
                self.writer.writerow([symbol, col, patterns[col]])


def read_symbols(filename):
    csvfile = open(filename, 'r')
    symbol_reader = csv.reader(csvfile, delimiter=",")
    symbol_reader.next()
    symbols = []

    for row in symbol_reader:
        if row[2] == 'n/a':
            continue

        lastsale = float(row[2])
        if lastsale > 1 and row[3].endswith('B'):
            symbols.append(row[0])

    return symbols


if __name__ == "__main__":
    today = date.today()
    symbols = read_symbols("./data/NYSE_symbols.csv")
    analyzer = PatternAnalyzer(symbols, "./out/NYSE-PATTERNS-{}.csv".format(today.isoformat()))
    analyzer.analyze()

    symbols = read_symbols("./data/NASDAQ_symbols.csv")
    analyzer = PatternAnalyzer(symbols, "./out/NASDAQ-PATTERNS-{}.csv".format(today.isoformat()))
    analyzer.analyze()