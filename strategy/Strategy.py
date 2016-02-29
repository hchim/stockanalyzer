import pandas as pd

import analysis.indicator_feature as indfr
from analysis.basic import daily_prices_to_weekly_prices

class Strategy(object):

    def __init__(self, features, week_features=None, allow_short=True, start_value=1000000):
        """
        Parameters
        -----------
        features: dict
            Format: [("feature_function_name", {feature parameters})]
        week_features: dict
        """
        self.feature_params = features
        self.week_feature_params = week_features
        self.allow_short = allow_short
        self.start_value = start_value


    def __calculate_features(self, feature_params, prices):
        if feature_params is None:
            return None

        features = pd.DataFrame(index=prices.index)
        for f in feature_params:
            values = getattr(indfr, f[0])(prices, f[1])
            features = features.join(values.to_frame())
            features.rename(columns={features.columns[-1]: f[0]}, inplace=True)

        return features


    def generate_orders(self, prices, symbol):
        self.prices = prices
        self.features = self.__calculate_features(self.feature_params, prices)
        if self.week_feature_params is not None:
            self.week_prices = daily_prices_to_weekly_prices(prices)
            self.week_features = self.__calculate_features(self.week_feature_params, self.week_prices)

        cash = self.start_value
        long_shares = short_shares = 0
        orders = []
        week_index = 0
        pre_week = prices.index[0].isocalendar()[1]
        self.curr_week_features = None

        for date in prices.index:
            if self.week_feature_params is not None:
                week = date.isocalendar()[1]
                if week != pre_week:
                    self.curr_week_features = self.week_features.iloc[week_index]
                    week_index += 1
                    pre_week = week

                if self.curr_week_features is None:
                    continue

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