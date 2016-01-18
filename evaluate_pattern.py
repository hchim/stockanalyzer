from analysis.candlestick_pattern import candlestick_patterns, PATTERNS
from utils.webdata import get_data_of_symbol
from datetime import date

import numpy as np
import csv

patterns = PATTERNS.keys()

def get_symbols(filename):
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


def analyze_symbols(symbols):
    number = 0
    total_bull_correct = np.zeros(len(patterns))
    total_bull_wrong = np.zeros(len(patterns))
    total_bear_correct = np.zeros(len(patterns))
    total_bear_wrong = np.zeros(len(patterns))

    for symbol in symbols:
        print symbol
        bc, bw, bco, bwr = evaluate_pattern(symbol)
        if bc is None:
            continue

        for i in range(len(bc)):
            if not np.isnan(bc[i]):
                total_bull_correct[i] += bc[i]
                total_bull_wrong[i] += bw[i]
            if not np.isnan(bco[i]):
                total_bear_correct[i] += bco[i]
                total_bear_wrong[i] += bwr[i]
        number += 1

    sum_bull = total_bull_correct + total_bull_wrong
    sum_bear = total_bear_correct + total_bear_wrong
    pgain = total_bull_correct*1.0/sum_bull
    plose = total_bear_correct*1.0/sum_bear

    keys = patterns
    for i in range(len(keys)):
        print keys[i], ": ", pgain[i], " ", sum_bull[i], " ", plose[i], " ", sum_bear[i]


def count_signals(signals, gain):
    signals = signals[:-5]
    gain = gain[:-5]
    col_len = len(signals.columns)
    count_bull_correct = np.zeros(col_len)
    count_bull_wrong = np.zeros(col_len)
    count_bear_correct = np.zeros(col_len)
    count_bear_wrong = np.zeros(col_len)

    for date in gain.index:
        for i in range(col_len):
            if signals.loc[date, signals.columns[i]] > 0:
                # stat the bull signal of the symbol
                if gain[date] > 0:
                    count_bull_correct[i] += 1
                else:
                    count_bull_wrong[i] += 1
            elif signals.loc[date, signals.columns[i]] < 0:
                # stat the bear signal of the symbol
                if gain[date] < 0:
                    count_bear_correct[i] += 1
                else:
                    count_bear_wrong[i] += 1

    return count_bull_correct, count_bull_wrong, count_bear_correct, count_bear_wrong


def evaluate_pattern(symbol):
    startdate = '2014-01-01'
    enddate = date.today().isoformat()
    prices = get_data_of_symbol(symbol, startdate, enddate, fill_empty=False)
    if prices is None:
        return None, None, None, None

    prices.dropna(how="any")
    if len(prices.index) <= 5:
        return None, None, None, None

    pattern_signals = candlestick_patterns(prices, patterns)
    close = prices['Close']
    gain5 = close.shift(-5)/close - 1

    return count_signals(pattern_signals, gain5)


if __name__ == "__main__":
    symbols = get_symbols("./data/NYSE_symbols.csv")
    analyze_symbols(symbols)