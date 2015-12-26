import math
import numpy as np

from Learner import Learner
from EnsembleLearner import EnsembleLearner


class BagLearner(Learner):

    def __init__(self, type, args, bags=5, boost=False, percent=0.65, rmse_percent=0.5):
        """
        Create the bootstrap bagging learner.

        Parameters
        ----------
        type: string
            The type of the learner to use, it could be LR, KNN
        args: map
            The arguments used to create the learners.
        bags: int
            The number of bags.
        boost: boolean
            Use Ada boost to train the models
        percent: float
            Percent of random data to chose.
        rmse_percent: float
            If distance is more than <bias_percent> of rmse, the point is bias point.
        """
        objs = []
        for i in range(bags):
            objs.append(EnsembleLearner.create_learner(type, args))

        self.learners = objs
        self.bags = bags
        self.boost = boost
        self.percent = percent
        self.rmse_percent = rmse_percent


    def get_random_data(self, xdata, ydata, bias=None):
        size = len(xdata)
        num = math.floor(self.percent * size)
        index = np.random.choice(size, size=num)
        if bias is not None:
            for i in bias:
                np.append(index, [i])

        r_xdata = [xdata[i] for i in index]
        r_ydata = [ydata[i] for i in index]

        return np.array(r_xdata), np.array(r_ydata), index


    def find_bias_points(self, ydata, predict, index):
        """
        Find the bias points.

        Parameters
        ----------
        ydata: np.array
        predict: np.array
        index: array
            Indexes of the random values.
        distances: array

        Returns
        ----------
        bias : array
            the indexes of the bias points.
        """
        rmse, corr = Learner.evaluate_predicated(ydata, predict)
        rmse_threshold = rmse * (1 + self.rmse_percent)
        bias = []
        for i in range(len(index)):
            if math.fabs(ydata[i] - predict[i]) > rmse_threshold:
                bias.append(index[i])

        return bias


    def train(self, xdata, ydata):
        bias = None

        for learner in self.learners:
            r_xdata, r_ydata, index = self.get_random_data(xdata, ydata, bias)
            learner.train(r_xdata, r_ydata)
            if self.boost:
                bias = self.find_bias_points(r_ydata, learner.query(r_xdata), index)


    def query(self, points):
        predict = None
        for learner in self.learners:
            temp = learner.query(points)
            if predict is None:
                predict = temp
            else:
                predict = predict + temp

        return predict/self.bags