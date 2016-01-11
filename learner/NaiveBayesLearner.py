from learner.Learner import Learner
import pandas as pd


class NaiveBayesLearner(Learner):


    def __init__(self):
        self.py = {}
        self.pa = []


    def calculate_pa(self, ai, datay, count_y):
        """
        Calculate P(ai|yi)
        """
        count = {}
        for i in range(len(ai.index)):
            a = ai.iloc[i]
            y = datay.iloc[i]
            if not a in count:
                count[a] = {}

            if y in count[a]:
                count[a][y] += 1
            else:
                count[a][y] = 1

        for a in count.keys():
            for y in count[a].keys():
                count[a][y] = count[a][y] * 1.0 / count_y[y]

        return count


    def train(self, datax, datay):
        """
        Calculate P(yi) and P(ai|yi).
        """
        if isinstance(datay, pd.DataFrame):
            datay = datay.iloc[:, 0]

        cy = {}
        for date in datay.index:
            y = datay.loc[date]
            if y in cy:
                cy[y] += 1
            else:
                cy[y] = 1

        for i in range(len(datax.columns)):
            pa = self.calculate_pa(datax.iloc[:, i], datay, cy)
            self.pa.append(pa)

        length = len(datax) * 1.0
        self.py = cy
        for y in cy.keys():
            self.py[y] = cy[y] / length


    def query(self, points):
        """
        P(x|yi)*P(yi) = P(yi) * P(a0|yi) * ... P(am|yi)
        """
        results = []
        for date in points.index:
            results.append(self.query_y(points.loc[date]))

        return pd.DataFrame(results, index=points.index, columns=["Y"])


    def query_y(self, point):
        max_val = 0
        max_y = None
        for y in self.py.keys():
            val = self.py[y]
            for i in range(len(self.pa)):
                val *= self.pa[i][point[i]][y]
            if val > max_val:
                max_val = val
                max_y = y

        return max_y