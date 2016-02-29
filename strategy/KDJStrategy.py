from strategy.Strategy import Strategy

class KDJStrategy(Strategy):

    def __init__(self):
        features = [
            ("reverse_kdj_cross", {"window":14, "thresholds": [30, 70]}),
            # ("reverse_kdj_over_sell_buy", {"window":14, "thresholds": [0, 100]}),
        ]
        week_features = [
            ("trend_stoch", {"windows": [14, 3, 3]})
        ]
        Strategy.__init__(self, features, week_features, allow_short=False)


    def is_buy_signal(self):
        return self.curr_week_features[0] == 1 and self.curr_features[0] == 1


    def is_sell_signal(self):
        return self.curr_features[0] == -1


    def is_short_signal(self):
        return self.curr_week_features[0] == -1 and self.curr_features[0] == -1


    def is_cover_signal(self):
        return self.curr_features[0] == 1
