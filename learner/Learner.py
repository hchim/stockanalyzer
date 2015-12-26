import math
import numpy as np


class Learner(object):

    def __init__(self):
        pass


    def train(self, datax, datay):
        """
        Train the learner.

        Parameters
        ----------
        datax: np.array
        datay: np.array
        """
        pass


    def query(self, points):
        """
        Predict the y values of the given points.

        Parameters
        ----------
        points : np.array
            x values, each row is a query

        Returns
        ----------
        values: np.array
            predicted values
        """
        return None


    @staticmethod
    def evaluate_predicated(test, predict):
        """
        Calculate the metrics that evaluate the Learning algorithm with the predicted result.

        Parameters
        ----------
        test: np.array
        predict: np.array

        Returns
        ----------
        rmse: float
            root-mean-square error
        corr: float
            correlation between test and predict
        """
        rmse = math.sqrt(((test - predict) ** 2).sum()/test.shape[0])
        corr = np.corrcoef(predict, y=test)
        return rmse, corr[0, 1]


    @staticmethod
    def euclidean_distance(x, y):
        """
        Calculate the euclidean distance of two instances.

        Parameters
        -----------

        x: np.array
        y: np.array

        Returns
        ----------
        distance : float
            the distance of these two instances
        """
        temp = (x - y) ** 2
        return math.sqrt(temp.sum())