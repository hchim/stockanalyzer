from analysis.candlestick_pattern import candlestick_patterns, GOOD_PATTERNS, PATTERNS
from utils.webdata import get_data_of_symbol

import numpy as np
import csv

patterns = PATTERNS.keys()


def analyze_symbols(filename, callback):
    csvfile = open(filename, 'r')
    symbol_reader = csv.reader(csvfile, delimiter=",")
    symbol_reader.next()

    number = 0
    total_gain = np.zeros(len(patterns))
    total_lose = np.zeros(len(patterns))
    for row in symbol_reader:
        if row[2] == 'n/a':
            continue

        lastsale = float(row[2])
        if lastsale > 1 and row[3].endswith('B'):
            print row
            gain, lose = callback(row[0])
            if gain is None:
                continue

            for i in range(len(gain)):
                if not np.isnan(gain[i]):
                    total_gain[i] += gain[i]
                    total_lose[i] += lose[i]
            number += 1

    sum = total_lose + total_gain
    pgain = total_gain/sum
    plose = total_lose/sum

    keys = patterns
    for i in range(len(keys)):
        print keys[i], ": ", pgain[i], " ", plose[i], " ", sum[i]


def count_signals(signals, gain):
    signals = signals[:-5]
    gain = gain[:-5]
    col_len = len(signals.columns)
    count_bull = np.zeros(col_len)
    count_bear = np.zeros(col_len)
    for date in gain.index:
        if gain[date] > 0:
            for i in range(col_len):
                if signals.loc[date, signals.columns[i]] > 0:
                    count_bull[i] += 1
        else:
            for i in range(col_len):
                if signals.loc[date, signals.columns[i]] < 0:
                    count_bear[i] += 1

    return count_bull, count_bear


def evaluate_pattern(symbol):
    startdate = '2014-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol(symbol, startdate, enddate, fill_empty=False)
    if prices is None:
        return None, None

    prices.dropna(how="any")
    if len(prices.index) <= 5:
        return None, None

    pattern_signals = candlestick_patterns(prices, patterns)
    close = prices['Close']
    gain5 = close.shift(-5)/close - 1

    return count_signals(pattern_signals, gain5)


if __name__ == "__main__":
    analyze_symbols("./data/NYSE_symbols.csv", evaluate_pattern)