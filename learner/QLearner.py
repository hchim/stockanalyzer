import numpy as np
import pandas as pd
import random as rand

from learner.Learner import Learner


class QLearner(object):

    def __init__(self, num_actions = 3, alpha = 0.5, gamma = 0.9,
                 r_action_rate = 0.95, r_action_decay_rate = 0.99):
        """
        Parameters
        ----------
        num_states: int
        num_actions: int
        alpha: float
            learning rate, ranges from 0 to 1
        gamma: float
            discount rate, ranges frm 0 to 1
        r_action_rate: float
            the probability of selecting a random action at each step
        r_action_decay_rate: float
            random action decay rate
        """
        # init the values of the Q table as NaN
        self.table = {}

        self.alpha = alpha
        self.gamma = gamma
        self.num_actions = num_actions
        self.r_action_rate = r_action_rate
        self.r_action_decay_rate = r_action_decay_rate
        self.state = 0
        self.action = 0


    def get_q_element(self, state):
        """
        Get q table elements of the given state. If it does not exit, init it with the default values.
        For some of the states, there are not too many training samples. So, it is better to maintain
        a separate epsilon for each state. When make predictions, the epsilon value also shows whether
        the state was fully trained.
        """
        if not self.table.has_key(state):
            self.table[state] = {
                "q_vals" : np.zeros(self.num_actions), # Q values of actions
                "epsilon" : self.r_action_rate         # epsilon of this state
            }

        return self.table.get(state)


    def get_q_value(self, state, action):
        """
        Get the corresponding q value of the given state and action.
        """
        qs = self.get_q_element(state)
        return qs["q_vals"][action]


    def chose_action(self, state):
        """
        Query the best action with the given state and update the state and action
        of the learner to this new state and the corresponding new action.
        """
        qs = self.get_q_element(state)

        # epsilon-greedy + softmax
        if rand.random() < qs["epsilon"]:
            # TODO use softmax
            action = rand.choice(range(len(qs)))
        else:
            action = qs["q_vals"].argmax()

        # update random action rate
        qs["epsilon"] *= self.r_action_decay_rate

        return action, qs["q_vals"][action]


    def learn(self, new_state, reward):
        """
        Update the Q value for the previous state and action. Also, it invokes
        the query method to update the state and action of the learner.

        Parameters
        ----------
        new_state: int
        reward: int

        Returns
        new_action: int
        """
        pre_state = self.state
        pre_action = self.action
        qs = self.get_q_element(pre_state)
        # will update self.state and self.action
        new_action, q_val = self.chose_action(new_state)
        # update Q value for previous state and action
        qs["q_vals"][pre_action] = (1 - self.alpha) * qs["q_vals"][pre_action] \
            + self.alpha * (reward + self.gamma * q_val) # plus immediate reward and later reward
        # update to the new state and action
        self.state = new_state
        self.action = new_action

        return new_action


    def dump(self):
        keys = self.table.keys()
        keys = np.sort(keys)
        for key in keys:
            print key, " - ", self.get_q_element(key)["q_vals"]