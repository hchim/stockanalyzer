from learner.QLearner import QLearner
from analysis.indicators import discritized_indicators

import matplotlib.pyplot as plt
import pandas as pd

class QStrategy(object):


    def __init__(self, params, bin_num):
        self.learner = QLearner(r_action_rate=0.8)
        self.params = params
        self.bin_num = bin_num

    #TODO find a better reward function
    def calculate_reward(self, *args):
        pre_date = args[0]
        pre_action = args[1]
        date = args[2]
        pre_price = self.prices.loc[pre_date, 'Close']
        price = self.prices.loc[date, 'Close']

        if pre_action == 2:   # nothing
            return 0
        elif pre_action == 0: # buy
            return (price - pre_price) / pre_price
        else:                 # sell
            return (pre_price - price) / pre_price


    def train_learner(self, prices):
        self.prices = prices
        dist_inds = discritized_indicators(prices, self.params, self.bin_num)
        # TODO convergence check
        dest_q = []
        for i in range(0, 100):
            state = dist_inds.iloc[0]
            action = self.learner.chose_action(state)
            pre_date = dist_inds.index[0]

            for date in dist_inds.index[1:]:
                reward = self.calculate_reward(pre_date, action, date)
                state = dist_inds.loc[date]
                action = self.learner.learn(state, reward)
                pre_date = date
            dest_q.append(self.learner.get_q_value(state, action))

        self.dest_q = dest_q
        self.learner.dump()


    def predict(self, new_prices, num=1):
        self.prices = new_prices
        dist_inds = discritized_indicators(new_prices, self.params, self.bin_num)
        points = dist_inds.iloc[-num:]

        actions = []
        pre_date = dist_inds.index[len(dist_inds) - num - 1]
        action = self.learner.action

        for date in points.index:
            state = points.loc[date]
            reward = self.env.calculate_reward(pre_date, action, date)
            action = self.learn(state, reward)
            pre_date = date
            actions.append(action)

        return pd.DataFrame(actions, index=points.index, columns=["Action"])


    def plot_data(self):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(range(0, len(self.dest_q)), self.dest_q)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Q')

        plt.show()