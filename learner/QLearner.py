import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, num_states, num_actions = 3, alpha = 0.5, gamma = 0.9,
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
        self.table = np.zeros([num_states, num_actions])
        self.alpha = alpha
        self.gamma = gamma
        self.r_action_rate = r_action_rate
        self.r_action_decay_rate = r_action_decay_rate
        self.state = 0
        self.action = 0


    def query_set_state(self, state):
        """
        Query the best action with the given state and update the state and action
        of the learner to this new state and the corresponding new action.
        """
        qs = self.table[state]

        if rand.random() < self.r_action_rate:
            max = qs.max()
            indices = [i for i in range(len(qs)) if qs[i] == max]
            action = rand.choice(indices)
        else:
            action = qs.argmax()

        # update to the new state and action
        self.state = state
        self.action = action
        # update random action rate
        self.r_action_rate *= self.r_action_decay_rate
        return action


    def query(self, new_state, reward):
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
        new_action = self.query_set_state(new_state)
        # update Q value for previous state and action
        self.table[pre_state][pre_action] = (1 - self.alpha) * self.get_q(pre_state, pre_action) \
            + self.alpha * (reward + self.gamma * self.get_q(new_state, new_action)) # plus immediate reward and later reward

        return new_action


    def get_q(self, state, action):
        return self.table[state][action]