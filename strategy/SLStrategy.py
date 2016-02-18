import pandas as pd

import analysis.indicators as ind
from analysis.basic import normalize
"""
This class defines the trading strategy. The x and y values of the trading strategy.

x:  X is a N dimension vector that composed by a group of normalized indicators.
    The value of each indicator ranges from -1 to 1, so that a single indcator
    cannot overwhelm the result.
y:  Y is either the future T day return or the normalized price in after T days.
"""

TARGET_PRICE = "PRICE"
TARGET_RETURN = "RETURN"

class SLStrategy(object):

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, indicators, learner, target=TARGET_PRICE, target_period=3):
        """
        Parameters
        -----------
        indicators: [dict]
            the indicators to compare. for example:
            {"name": "obv", "column":"OBV", "normalize":True, "params": None}
            name: function name
            column: the column of the indicator value
            normalize: normalize the value
            params: parameters of the indicator
        target: String
            RETURN: find the correlation with the return after T days (T is the target period).
            PRICE: find the correlation with the price after T days.
        target_period: int
        """
        self.indicators = indicators
        self.learner = learner
        self.target = target
        self.target_period = target_period
        self.base_price = None


    def train_learner(self, prices):
        self.base_price = prices["Close"][0]
        x = self.calculate_x(prices)
        y = self.calculate_y(prices)

        vals = y.to_frame().join(x, how="inner")
        vals.dropna(inplace=True)
        self.prices = prices
        self.values = vals
        self.corr = vals.corr().values[0, 1:]
        self.learner.train(vals[vals.columns[1:]].values, vals[vals.columns[0]].values)


    def calculate_x(self, prices):
        x = pd.DataFrame(index=prices.index)

        for indicator in self.indicators:
            ind_vals = getattr(ind, indicator["name"])(prices, indicator["params"])
            ind_vals = ind_vals[indicator["column"]].dropna()
            if indicator["normalize"] and ind_vals[0] != 0:
                ind_vals = normalize(ind_vals)
            x = x.join(pd.DataFrame(ind_vals.values, index=ind_vals.index, columns=[indicator["column"]]), how="inner")

        return x


    def calculate_y(self, prices):
        values = None
        close = prices['Close']

        if self.target == TARGET_RETURN:
            values = close.shift(-1 * self.target_period)/close - 1
        elif self.target == TARGET_PRICE:

            values = normalize(close)
            values = values.shift(-1 * self.target_period)

        return values.dropna()


    def predict(self, new_prices, num=1):
        """
        Predict the future return with the given prices for the nearest <num> days.
        For evaluation the strategy, num is the length of the test date.
        For normal usage, num is just one. We use today's close price to anticipate
        the return in the next 5 days.

        Parameters
        ----------
        new_prices: DataFrame
            previous daily prices, we use these prices to calculate the indicators (x)
            in the recent days. new prices must be started from the same date as training
            prices because both indicator value and its normalized value may be different
            with different start date.
        num: int

        Returns
        ----------
        y: np.array
            the predicted y.
        """
        x = self.calculate_x(new_prices)
        x = x.iloc[-num:, :]
        return self.learner.query(x.values)


    def __predicted_return(self, price, predicted):
        if self.target == TARGET_RETURN:
            return predicted
        else:
            predicted_price = (predicted + 1) * self.base_price
            return (predicted_price - price) / price


    def generate_orders(self, symbol, new_prices, num=1,
                        buy_point=0.01, sell_point=0.05, short_point=-0.05, cover_point=-0.01,
                        allow_short=True, start_value=1000000,
                        save_to_file=False, filepath="orders.csv"):
        dates = new_prices.index[-num:]
        predicted = self.predict(new_prices, num)

        cash = start_value
        long_shares = short_shares = 0
        orders = []

        if save_to_file:
            file = open(filepath, 'w')
            file.write('Date,Symbol,Order,Shares\r\n')

        for i in range(len(dates)):
            date = dates[i]
            close = new_prices.loc[date, 'Close']
            ret = self.__predicted_return(close, predicted[i])

            # long operations
            if long_shares == 0 and ret > buy_point:
                long_shares = round(cash / close, 0)
                cash -= long_shares * close
                if save_to_file:
                    file.write("{0},{1},BUY,{2}\r\n".format(date.strftime(self.DATE_FORMAT), symbol, long_shares))
                orders.append((date, symbol, 'BUY', long_shares))
                continue

            if long_shares >0 and ret <= sell_point:
                cash += long_shares * close
                if save_to_file:
                    file.write("{0},{1},SELL,{2}\r\n".format(date.strftime(self.DATE_FORMAT), symbol, long_shares))
                orders.append((date, symbol, 'SELL', long_shares))
                long_shares = 0
                continue

            if not allow_short:
                continue

            if short_shares == 0 and ret < short_point:
                short_shares = round(cash / close, 0)
                cash += short_shares * close
                if save_to_file:
                    file.write("{0},{1},SELL,{2}\r\n".format(date.strftime(self.DATE_FORMAT), symbol, short_shares))
                orders.append((date, symbol, 'SELL', short_shares))
                continue

            if short_shares > 0 and ret >= cover_point:
                cash -= short_shares * close
                if save_to_file:
                    file.write("{0},{1},BUY,{2}\r\n".format(date.strftime(self.DATE_FORMAT), symbol, short_shares))
                orders.append((date, symbol, 'BUY', short_shares))
                short_shares = 0

        df = pd.DataFrame(orders, columns=['Date', 'Symbol', 'Order', 'Shares'])
        return df