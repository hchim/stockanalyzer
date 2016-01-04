import pandas as pd

from analysis.indicators import calculate_indicators


class Strategy(object):

    def __init__(self, indicator_params):
        self.indicator_params = indicator_params


    def generate_orders(self, prices, symbol, allow_short=True, start_value=1000000):
        self.prices = prices
        self.indicators = calculate_indicators(prices, self.indicator_params)

        cash = start_value
        long_shares = short_shares = 0
        dates = self.indicators.index
        orders = []
        pre_inds = None
        pre_prices = None

        for date in dates:
            inds = self.indicators.loc[date]
            curr_prices = prices.loc[date, :]
            close = prices.loc[date, 'Close']

            # long operations
            if long_shares == 0 and self.is_buy_signal(inds, pre_inds, curr_prices, pre_prices):
                long_shares = round(cash / close, 0)
                cash -= long_shares * close
                orders.append((date, symbol, 'BUY', long_shares))
            elif long_shares > 0 and self.is_sell_signal(inds, pre_inds, curr_prices, pre_prices):
                cash += long_shares * close
                orders.append((date, symbol, 'SELL', long_shares))
                long_shares = 0

            if allow_short:
                if short_shares == 0 and self.is_short_signal(inds, pre_inds, curr_prices, pre_prices):
                    short_shares = round(cash / close, 0)
                    cash += short_shares * close
                    orders.append((date, symbol, 'SELL', short_shares))
                elif short_shares > 0 and self.is_cover_signal(inds, pre_inds, curr_prices, pre_prices):
                    cash -= short_shares * close
                    orders.append((date, symbol, 'BUY', short_shares))
                    short_shares = 0

            pre_inds = inds
            pre_prices = curr_prices

        df = pd.DataFrame(orders, columns=['Date', 'Symbol', 'Order', 'Shares'])
        return df


    def is_buy_signal(self, inds, pre_inds, prices, pre_prices):
        return False


    def is_sell_signal(self, inds, pre_inds, prices, pre_prices):
        return False


    def is_short_signal(self, inds, pre_inds, prices, pre_prices):
        return False


    def is_cover_signal(self, inds, pre_inds, prices, pre_prices):
        return False