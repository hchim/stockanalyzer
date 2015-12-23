from utils.webdata import get_data_of_symbol, get_adj_close_of_symbols
from utils.draw import plot_single_symbol, plot_multi_symbols
from strategy.sma13_strategy import generate_sma13_orders
from strategy.bb_strategy import generate_bb_orders

def test_webdata_single():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    symbols = ['AAPL', 'AMZN']
    prices = get_adj_close_of_symbols(symbols, startdate, enddate)
    plot_multi_symbols(prices, normalize=True)


def test_webdata_multiple():
    startdate = '2015-01-01'
    enddate = '2015-12-23'
    prices = get_data_of_symbol('AAPL', startdate, enddate, fill_empty=False)
    plot_single_symbol(prices, indicators={
        "BB" : None,
        "MACD" : None,
        "SMA" : [5, 13]
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


if __name__ == "__main__":
    # test_webdata_single()
    # test_webdata_multiple()
    # test_sma13_orders()
    test_bb_orders()