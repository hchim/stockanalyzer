import pandas as pd
import numpy as np

from utils.webdata import get_data_of_symbol, get_adj_close_of_symbols
from utils.draw import plot_single_symbol, plot_multi_symbols, normalize_data
from strategy.sma13_strategy import generate_sma13_orders
from strategy.bb_strategy import generate_bb_orders
from analysis.portfolio import find_optimal_allocations, get_portfolio_stats, get_portfolio_value
from simulator.tradesimulator import compute_portvals

def test_webdata_multiple():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['AAPL', 'AMZN']
    prices = get_adj_close_of_symbols(symbols, startdate, enddate)
    plot_multi_symbols(prices, normalize=True)


def test_webdata_single():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol('AAPL', startdate, enddate, fill_empty=False)
    plot_single_symbol(prices, indicators={
        "VOLUME" : None,
        "BB" : None,
        "MACD" : None,
        "SMA" : {'windows': [60, 120]},
        "RSI" : None
    })


def test_sma13_orders():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol('AAPL', startdate, enddate, fill_empty=False)
    orders = generate_sma13_orders(prices, 'AAPL')
    plot_single_symbol(prices, indicators={
        "MACD" : None,
        "SMA" : [5, 13]
    }, orders=orders)


def test_bb_orders():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol('AAPL', startdate, enddate, fill_empty=False)
    orders = generate_bb_orders(prices, 'AAPL', save_to_file=True, filepath="./out/bb_orders_AAPL.csv")
    plot_single_symbol(prices, indicators={
        "BB" : None
    }, orders=orders)


def test_portfolio_optimize():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['GOOG', 'AAPL', 'AMZN', 'FB']
#    symbols = ['BABA', 'JD', 'VIPS', 'JMEI']
    prices_all = get_adj_close_of_symbols(symbols, startdate, enddate)  # automatically adds SPY
    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # get optimal allocations
    allocs = find_optimal_allocations(prices)
    allocs = allocs / np.sum(allocs)  # normalize allocations

    port_val = get_portfolio_value(prices, allocs)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    # Print statistics
    print "Symbols:", symbols
    print "Optimal allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility:", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    normed_SPY = normalize_data(prices_SPY)
    df_temp = pd.concat([port_val, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_multi_symbols(df_temp, title="Daily Portfolio Value and SPY")


def test_simulator():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbol = 'AMZN'
    prices = get_data_of_symbol(symbol, startdate, enddate, fill_empty=False)
    orders = generate_sma13_orders(prices, symbol)
    # Process orders
    portvals = compute_portvals(startdate, enddate, orders=orders, leverage=2.0)

    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals[portvals.columns[0]])

    # Print statistics
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility:", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    prices_SPY = get_adj_close_of_symbols([], startdate, enddate)
    df_temp = pd.concat([portvals, prices_SPY], axis=1)
    plot_multi_symbols(normalize_data(df_temp), title="{} and SPY".format(symbol))


if __name__ == "__main__":
    test_webdata_single()
    # test_webdata_multiple()
    # test_sma13_orders()
    # test_bb_orders()
    # test_portfolio_optimize()
    # test_simulator()