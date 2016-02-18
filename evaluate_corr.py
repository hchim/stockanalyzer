from simulator.CorrEvaluator import CorrEvaluator

PERIOD = {"startdate": "2015-01-01", "enddate":"2015-12-30"}

SYMBOLS_IT = ['AAPL', 'AMZN', 'GOOG', 'FB', 'IBM', 'MSFT', 'QCOM', 'ORCL', 'NFLX',
              'INTL', 'SAP', 'CRM', 'VMW', 'PANW', 'CA', 'INTU', 'BABA', 'JD',
              'BIDU']


def evaluate_obv_corr():
    """
    {'symbol': 'AAPL', 'corr': 0.83000011790853911}
    {'symbol': 'AMZN', 'corr': 0.96778961159707622}
    {'symbol': 'GOOG', 'corr': 0.52723542480425323}
    {'symbol': 'FB', 'corr': 0.95549174890880073}
    {'symbol': 'IBM', 'corr': 0.93702051142527687}
    {'symbol': 'MSFT', 'corr': 0.33092979045175203}
    {'symbol': 'QCOM', 'corr': 0.93282681778049792}
    {'symbol': 'ORCL', 'corr': 0.90167880117786103}
    {'symbol': 'NFLX', 'corr': 0.36892367272860982}
    {'symbol': 'INTL', 'corr': 0.66192801795852829}
    {'symbol': 'SAP', 'corr': 0.80120494527971853}
    {'symbol': 'CRM', 'corr': 0.89148366971041992}
    {'symbol': 'VMW', 'corr': 0.96513548650897207}
    {'symbol': 'PANW', 'corr': 0.89052671172261733}
    {'symbol': 'CA', 'corr': 0.71627179889853732}
    {'symbol': 'INTU', 'corr': 0.45195387457698721}
    {'symbol': 'BABA', 'corr': 0.87857410202463393}
    {'symbol': 'JD', 'corr': 0.790562434712753}
    {'symbol': 'BIDU', 'corr': 0.86062120584263258}
    CORR: AVG:0.771587302317 MIN:0.330929790452 MAX:0.967789611597 MEDIAN:0.860621205843
    """
    indicator = {"name": "obv", "column": "OBV", "params":None, "normalize": True}
    evaluator = CorrEvaluator(PERIOD["startdate"], PERIOD["enddate"], symbols=SYMBOLS_IT,
                              indicator=indicator, target="PRICE", target_period=3)
    evaluator.start()
    evaluator.dump_report()


def evaluate_sma_corr():
    """
    {'symbol': 'AAPL', 'corr': 0.87976855970759571}
    {'symbol': 'AMZN', 'corr': 0.98552634349847157}
    {'symbol': 'GOOG', 'corr': 0.9585213929323394}
    {'symbol': 'FB', 'corr': 0.96272100627065449}
    {'symbol': 'IBM', 'corr': 0.95225926358467838}
    {'symbol': 'MSFT', 'corr': 0.91845306783862624}
    {'symbol': 'QCOM', 'corr': 0.95778661529668174}
    {'symbol': 'ORCL', 'corr': 0.9313294682942469}
    {'symbol': 'NFLX', 'corr': 0.95995146919746988}
    {'symbol': 'INTL', 'corr': 0.95666521801557813}
    {'symbol': 'SAP', 'corr': 0.91270378813265096}
    {'symbol': 'CRM', 'corr': 0.93821706439580799}
    {'symbol': 'VMW', 'corr': 0.95874358067948873}
    {'symbol': 'PANW', 'corr': 0.94009303399354294}
    {'symbol': 'CA', 'corr': 0.91391557642603727}
    {'symbol': 'INTU', 'corr': 0.85589118980128831}
    {'symbol': 'BABA', 'corr': 0.91820254340147522}
    {'symbol': 'JD', 'corr': 0.90983442312270357}
    {'symbol': 'BIDU', 'corr': 0.93089784709688539}
    CORR: AVG:0.933762181668 MIN:0.855891189801 MAX:0.985526343498 MEDIAN:0.938217064396
    """
    indicator = {"name": "sma", "column": "SMA5", "params":{"windows":[5]}, "normalize": True}
    evaluator = CorrEvaluator(PERIOD["startdate"], PERIOD["enddate"], symbols=SYMBOLS_IT, thread_number=1,
                              indicator=indicator, target="PRICE", target_period=3)
    evaluator.start()
    evaluator.dump_report()


def evaluate_bb_corr():
    """
    {'symbol': 'AAPL', 'corr': 0.73945855812922834}
    {'symbol': 'AMZN', 'corr': 0.96542708640373531}
    {'symbol': 'GOOG', 'corr': 0.92854948178497565}
    {'symbol': 'FB', 'corr': 0.92997546381321528}
    {'symbol': 'IBM', 'corr': 0.91579238821930475}
    {'symbol': 'MSFT', 'corr': 0.85357971951411338}
    {'symbol': 'QCOM', 'corr': 0.92485014942941302}
    {'symbol': 'ORCL', 'corr': 0.90889378498790041}
    {'symbol': 'NFLX', 'corr': 0.92299875116207541}
    {'symbol': 'INTL', 'corr': 0.8279944207132095}
    {'symbol': 'SAP', 'corr': 0.75982349093342316}
    {'symbol': 'CRM', 'corr': 0.88710505717323318}
    {'symbol': 'VMW', 'corr': 0.91653158333315643}
    {'symbol': 'PANW', 'corr': 0.83951700987226652}
    {'symbol': 'CA', 'corr': 0.88883096178903886}
    {'symbol': 'INTU', 'corr': 0.67365433004622888}
    {'symbol': 'BABA', 'corr': 0.77997067051939573}
    {'symbol': 'JD', 'corr': 0.78097833153411533}
    {'symbol': 'BIDU', 'corr': 0.83434671954126605}
    CORR: AVG:0.856751471521 MIN:0.673654330046 MAX:0.965427086404 MEDIAN:0.887105057173
    """
    indicator = {"name": "bollinger_bands", "column": "Middle", "params":{"window":20}, "normalize": True}
    evaluator = CorrEvaluator(PERIOD["startdate"], PERIOD["enddate"], symbols=SYMBOLS_IT, thread_number=1,
                              indicator=indicator, target="PRICE", target_period=3)
    evaluator.start()
    evaluator.dump_report()


def evaluate_corr():
    indicator = {"name": "macd", "column": "MACD", "params":{"windows": [12, 26, 9]}, "normalize": True}
    evaluator = CorrEvaluator(PERIOD["startdate"], PERIOD["enddate"], symbols=SYMBOLS_IT, thread_number=1,
                              indicator=indicator, target="RETURN", target_period=3)
    evaluator.start()
    evaluator.dump_report()


if __name__ == "__main__":
    # evaluate_obv_corr()
    # evaluate_sma_corr()
    evaluate_corr()