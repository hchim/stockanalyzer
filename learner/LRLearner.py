import numpy as np
import math

from Learner import Learner

"""
Linear regression learner.
"""
class LRLearner(Learner):

    def __init__(self):
        pass


    def train(self, datax, datay):
        newdataX = np.ones([datax.shape[0], datax.shape[1] + 1])
        newdataX[:, 0:datax.shape[1]]=datax

        self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, datay)


    def query(self, points):
        return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]