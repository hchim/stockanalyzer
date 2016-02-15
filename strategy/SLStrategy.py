import pandas as pd
import matplotlib.pyplot as plt

from analysis.indicator_feature import indicator_features
"""
This class defines the trading strategy. The x and y values of the trading strategy.

x:  X is a N dimension vector that composed by a group of normalized indicators.
    The value of each indicator ranges from -1 to 1, so that a single indcator
    cannot overwhelm the result.
y:  Y is the future 5 day return because our strategy want to predict the future
    price.

"""

class Strategy(object):

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, indicators, learner):
        self.indicators = indicators
        self.learner = learner


    def train_learner(self, prices):
        x = self.calculate_x(prices)
        y = self.calculate_y(prices)

        vals = x.join(y)
        vals.dropna(inplace=True)
        self.prices = prices
        self.values = vals
        self.learner.train(vals[vals.columns[:-1]].values, vals[vals.columns[-1]].values)


    def calculate_x(self, prices):
        x = indicator_features(prices, self.indicators)
        return x


    def calculate_y(self, prices):
        """
        y = prices[t+5]/prices[t] - 1
        """
        close = prices['Close']
        y = close.shift(-5)/close - 1
        return y


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
            in the recent days and use the learner to predict the 5-days return.
        num: int
            predict the 5-days return

        Returns
        ----------
        5dayreturn: np.array
        """
        x = self.calculate_x(new_prices)
        x = x.iloc[-num:, :]
        return self.learner.query(x.values)


    def generate_orders(self, symbol, new_prices, num=1,
                        buy_point=0.01, sell_point=0.05, short_point=-0.05, cover_point=-0.01,
                        allow_short=True, start_value=1000000,
                        save_to_file=False, filepath="orders.csv"):
        dates = new_prices.index[-num:]
        predicted_return = self.predict(new_prices, num)

        cash = start_value
        long_shares = short_shares = 0
        orders = []

        if save_to_file:
            file = open(filepath, 'w')
            file.write('Date,Symbol,Order,Shares\r\n')

        for i in range(len(dates)):
            date = dates[i]
            close = new_prices.loc[date, 'Close']
            ret = predicted_return[i]

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


    def plot_data(self):
        dates = self.values.index
        prices = self.prices.loc[dates[0]:dates[-1], 'Close']

        fig, ax1 = plt.subplots()
        # two y axis
        ax2 = ax1.twinx()
        ax2.plot(dates, self.values.iloc[:, :-1])
        ax2.axhline(0, color="black")
        ax1.plot(dates, self.values.iloc[:, -1:], color="purple")

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Prices')

        plt.show()