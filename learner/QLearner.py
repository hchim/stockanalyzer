import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, num_states, num_actions = 3, alpha = 0.5, gamma = 0.9):
        """
        Parameters
        ----------
        num_states: int
        num_actions: int
        alpha: float
            learning rate, ranges from 0 to 1
        gamma: float
            discount rate, ranges frm 0 to 1
        """
        self.table = np.zeros([num_states, num_actions])
        self.alpha = alpha
        self.gamma = gamma
        self.state = 0
        self.action = 0


    def query(self, state):
        """
        Query the best action with the given state and update the state and action
        of the learner to this new state and the corresponding new action.
        """
        qs = self.table[state]
        max = qs.max()
        indices = [i for i in range(len(qs)) if qs[i] == max]

        if len(indices) > 1: # multiple max values
            action = rand.choice(indices)
        else:
            action = indices[0]

        # update to the new state and action
        self.state = state
        self.action = action

        return action


    def update(self, new_state, reward):
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
        # will update self.state and self.action
        new_action = self.query(new_state)
        # update Q value for previous state and action
        self.table[pre_state][pre_action] = (1 - self.alpha) * self.get_q(pre_state, pre_action) \
            + self.alpha * (reward + self.gamma * self.get_q(new_state, new_action)) # plus immediate reward and later reward

        return new_action


    def get_q(self, state, action):
        return self.table[state][action]