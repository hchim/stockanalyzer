import numpy as np
import scipy.optimize as spo


def get_portfolio_value(prices, allocs, start_val=1):
    """
    Compute the daily value of the portfolio with the given prices and initial allocations.

    :param prices: the prices of the stocks
    :param allocs: the allocations
    :param start_val: the start value of the portfolio

    :return: the daily value of the portfolio.
    """
    normalized_prices = prices/prices.iloc[0]          # all values divide the first row
    allocated = normalized_prices * allocs * start_val # calculate the allocations and values after the first day

    return allocated.sum(axis=1)


def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):
    """
    Calculate statistics on given portfolio values.

    :param port_val: the daily portfolio value
    :param daily_rf: daily risk-free rate of return
    :param samples_per_year: frequency of sampling

    :return: cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio
    """

    cum_ret = port_val[-1]/port_val[0] - 1
    daily_ret = port_val/port_val.shift(1) - 1
    avg_daily_ret = daily_ret.sum()/(len(daily_ret) - 1)
    std_daily_ret = daily_ret[1:].std()
    sharpe_ratio = np.sqrt(samples_per_year) * (avg_daily_ret - daily_rf)/std_daily_ret

    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio


def objective_fun_max_sharpe_ratio(allocs, prices):
    """
    The objective function that return max sharpe ratio.

    :param allocs: allocations of stocks
    :param prices: prices of stocks
    :return: negative sharpe_ratio
    """
    port_val = get_portfolio_value(prices, allocs, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    return sharpe_ratio * -1


def find_optimal_allocations(prices):
    """
    Find the optimal allocations for the portfolio, optimize sharpe ratio.

    :param prices: the prices of stocks

    :return: the allocation of the stocks
    """
    length = len(prices.columns)
    initial_allocs = np.empty(length)
    initial_allocs.fill(1.0/length)

    # create bounds
    bnds = []
    for i in range(length):
        bnds.append((0, 1))
    bnds = tuple(bnds)

    min_result = spo.minimize(
        objective_fun_max_sharpe_ratio, # objective function
        initial_allocs,                 # guess value
        args = (prices,),				# extra args passed to the objective fun
        method='SLSQP',                 # optimize algorithm to use
        # equality (type='eq') constraint, where you make a function that must equal zero
        constraints = ({ 'type': 'eq', 'fun': lambda x: 1 - np.sum(x) }),
        bounds = bnds,                  # the bounds of x
        options={'disp':True}           # display converge message
    )

    return min_result.x