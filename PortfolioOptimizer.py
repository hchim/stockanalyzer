import sys, numpy as np, pandas as pd
import analysis.portfolio as pot

from optparse import OptionParser
from datetime import date
from utils.webdata import get_close_of_symbols
from utils.draw import plot_multi_symbols, normalize_data

"""
This program is used to find the best portfolio allocation during the given period.
"""

def optimize_portfolio(symbols, startdate, enddate, compsymbol):
    prices = get_close_of_symbols(symbols, startdate, enddate, add_spy=False, fill_empty=False)  # automatically adds SPY
    prices_comp = get_close_of_symbols([compsymbol], startdate, enddate)

    # get optimal allocations
    allocs = pot.find_optimal_allocations(prices)
    allocs = allocs / np.sum(allocs)  # normalize allocations

    port_val = pot.get_portfolio_value(prices, allocs)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = pot.get_portfolio_stats(port_val)

    # Print statistics
    print "Range:", startdate, " - ", enddate
    print "Symbols:", symbols
    print "Optimal allocations:", ["%0.2f" % i for i in allocs]
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility:", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    normed_compsymbol = normalize_data(prices_comp[compsymbol])
    df_temp = pd.concat([port_val, normed_compsymbol], keys=['Portfolio', compsymbol], axis=1)
    plot_multi_symbols(df_temp, title="Daily Portfolio Value and {}".format(compsymbol))


def main():
    parser = OptionParser(usage="usage: %prog -s startdate [-e enddate] [-c compsymbol] symbol1 symbol2 ...",)
    parser.add_option("-s", "--startdate", dest="startdate",
                      help="the start date (YYYY-MM-DD) of symbol prices")
    parser.add_option("-e", "--enddate", dest="enddate", default=date.today().isoformat(),
                      help="the end date (YYYY-MM-DD) of symbol prices; the default value is today")
    parser.add_option("-c", "--compsymbol", dest="compsymbol", default='SPY',
                      help="the symbol to compare with; the default value is SPY")

    options, args = parser.parse_args()

    if options.startdate is None:
        parser.print_help()
        sys.exit()

    optimize_portfolio(args, options.startdate, options.enddate, options.compsymbol)


if __name__ == "__main__":
    main()