import pandas as pd

import analysis.indicator_feature as indfr


class Strategy(object):

    def __init__(self, features, allow_short=True, start_value=1000000):
        self.features_params = features
        self.allow_short = allow_short
        self.start_value = start_value


    def __calculate_features(self):
        if self.features_params is None:
            return None

        features = pd.DataFrame(index=self.prices.index)
        for f in self.features_params:
            values = getattr(indfr, f[0])(self.prices, f[1])
            features = features.join(values.to_frame())
            features.rename(columns={features.columns[-1]: f[0]}, inplace=True)

        return features


    def generate_orders(self, prices, symbol):
        self.prices = prices
        self.features = self.__calculate_features()

        cash = self.start_value
        long_shares = short_shares = 0
        dates = prices.index
        orders = []

        for date in dates:
            self.curr_features = self.features.loc[date]
            close = prices.loc[date, 'Close']

            if long_shares == 0 and self.is_buy_signal():
                long_shares = round(cash / close, 0)
                cash -= long_shares * close
                orders.append((date, symbol, 'BUY', long_shares))
            elif long_shares > 0 and self.is_sell_signal():
                cash += long_shares * close
                orders.append((date, symbol, 'SELL', long_shares))
                long_shares = 0

            if self.allow_short:
                if short_shares == 0 and self.is_short_signal():
                    short_shares = round(cash / close, 0)
                    cash += short_shares * close
                    orders.append((date, symbol, 'SELL', short_shares))
                elif short_shares > 0 and self.is_cover_signal():
                    cash -= short_shares * close
                    orders.append((date, symbol, 'BUY', short_shares))
                    short_shares = 0

        df = pd.DataFrame(orders, columns=['Date', 'Symbol', 'Order', 'Shares'])
        return df


    def is_buy_signal(self):
        return False


    def is_sell_signal(self):
        return False


    def is_short_signal(self):
        return False


    def is_cover_signal(self):
        return False