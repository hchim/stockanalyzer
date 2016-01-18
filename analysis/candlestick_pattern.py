import pandas as pd
import talib

PATTERNS = {
    "CDL2CROWS" : {"name" : "Two Crows", "signal_type": "bearish", "candles": 2},
    "CDL3BLACKCROWS" : {"name" : "Three Black Crows", "signal_type": "bearish", "candles": 3},
    "CDL3INSIDE" : {"name" : "Three Inside Up/Down", "signal_type": "bullish/bearish", "candles": 3},
    "CDL3LINESTRIKE" : {"name" : "Three-Line Strike", "signal_type": "bullish", "candles": 4},
    "CDL3OUTSIDE" : {"name" : "Three Outside Up/Down", "signal_type": "bullish/bearish", "candles": 3},
    "CDL3STARSINSOUTH" : {"name" : "Three Stars In The South", "signal_type": "bullish", "candles": 3},
    "CDL3WHITESOLDIERS" : {"name" : "Three Advancing White Soldiers", "signal_type": "bullish", "candles": 3},
    "CDLABANDONEDBABY" : {"name" : "Abandoned Baby", "signal_type": "bullish/bearish", "candles": 3},
    "CDLADVANCEBLOCK" : {"name" : "Advance Block", "signal_type": "bearish", "candles": 3},
    "CDLBELTHOLD" : {"name" : "Belt-hold", "signal_type": "bullish/bearish", "candles": 1},
    "CDLBREAKAWAY" : {"name" : "Breakaway", "signal_type": "bullish/bearish", "candles": 5},
    "CDLCLOSINGMARUBOZU" : {"name" : "Closing Marubozu", "signal_type": "bullish/bearish", "candles": 1},
    "CDLCONCEALBABYSWALL" : {"name" : "Concealing Baby Swallow", "signal_type": "bullish", "candles": 4},
    "CDLCOUNTERATTACK" : {"name" : "Counterattack", "signal_type": "bullish/bearish", "candles": 2},
    "CDLDARKCLOUDCOVER" : {"name" : "Dark Cloud Cover", "signal_type": "bearish", "candles": 2},
    "CDLDOJI" : {"name" : "Doji", "signal_type": "bullish", "candles": 1},
    "CDLDOJISTAR" : {"name" : "Doji Star", "signal_type": "bullish/bearish", "candles": 1},
    "CDLDRAGONFLYDOJI" : {"name" : "Dragonfly Doji", "signal_type": "bullish", "candles": 1},
    "CDLENGULFING" : {"name" : "Engulfing Pattern", "signal_type": "bullish/bearish", "candles": 2},
    "CDLEVENINGDOJISTAR" : {"name" : "Evening Doji Star", "signal_type": "bearish", "candles": 1},
    "CDLEVENINGSTAR" : {"name" : "Evening Star", "signal_type": "bearish", "candles": 3},
    "CDLGAPSIDESIDEWHITE" : {"name" : "Up/Down-gap side-by-side white lines", "signal_type": "bullish", "candles": 3},
    "CDLGRAVESTONEDOJI" : {"name" : "Gravestone Doji", "signal_type": "bullish/bearish", "candles": 1},
    "CDLHAMMER" : {"name" : "Hammer", "signal_type": "bullish", "candles": 1},
    "CDLHANGINGMAN" : {"name" : "Hanging Man", "signal_type": "bearish", "candles": 1},
    "CDLHARAMI" : {"name" : "Harami Pattern", "signal_type": "bullish/bearish", "candles": 2},
    "CDLHARAMICROSS" : {"name" : "Harami Cross Pattern", "signal_type": "bullish/bearish", "candles": 2},
    "CDLHIGHWAVE" : {"name" : "High-Wave Candle", "signal_type": "bullish/bearish", "candles": 1},
    "CDLHIKKAKE" : {"name" : "Hikkake Pattern", "signal_type": "bullish", "candles": 2},
    "CDLHIKKAKEMOD" : {"name" : "Modified Hikkake Pattern", "signal_type": "bullish/bearish", "candles": 1},
    "CDLHOMINGPIGEON" : {"name" : "Homing Pigeon", "signal_type": "bullish", "candles": 2},
    "CDLIDENTICAL3CROWS" : {"name" : "Identical Three Crows", "signal_type": "bearish", "candles": 3},
    "CDLINNECK" : {"name" : "In-Neck Pattern", "signal_type": "bearish", "candles": 2},
    "CDLINVERTEDHAMMER" : {"name" : "Inverted Hammer", "signal_type": "bullish", "candles": 1},
    "CDLKICKING" : {"name" : "Kicking", "signal_type": "bullish", "candles": 2},
    "CDLKICKINGBYLENGTH" : {"name" : "Kicking - bull/bear determined by the longer marubozu", "signal_type": "bullish/bearish", "candles": 1},
    "CDLLADDERBOTTOM" : {"name" : "Ladder Bottom", "signal_type": "bullish", "candles": 5},
    "CDLLONGLEGGEDDOJI" : {"name" : "Long Legged Doji", "signal_type": "bullish/bearish", "candles": 1},
    "CDLLONGLINE" : {"name" : "Long Line Candle", "signal_type": "bullish/bearish", "candles": 1},
    "CDLMARUBOZU" : {"name" : "Marubozu", "signal_type": "bullish/bearish", "candles": 1},
    "CDLMATCHINGLOW" : {"name" : "Matching Low", "signal_type": "bullish", "candles": 2},
    "CDLMATHOLD" : {"name" : "Mat Hold", "signal_type": "bullish/bearish", "candles": 5},
    "CDLMORNINGDOJISTAR" : {"name" : "Morning Doji Star", "signal_type": "bullish", "candles": 1},
    "CDLMORNINGSTAR" : {"name" : "Morning Star", "signal_type": "bullish", "candles": 3},
    "CDLONNECK" : {"name" : "On-Neck Pattern", "signal_type": "bearish", "candles": 2},
    "CDLPIERCING" : {"name" : "Piercing Pattern", "signal_type": "bullish", "candles": 2},
    "CDLRICKSHAWMAN" : {"name" : "Rickshaw Man", "signal_type": "bullish/bearish", "candles": 1},
    "CDLRISEFALL3METHODS" : {"name" : "Rising/Falling Three Methods", "signal_type": "bullish/bearish", "candles": 5},
    "CDLSEPARATINGLINES" : {"name" : "Separating Lines", "signal_type": "bullish", "candles": 2},
    "CDLSHOOTINGSTAR" : {"name" : "Shooting Star", "signal_type": "bearish", "candles": 1},
    "CDLSHORTLINE" : {"name" : "Short Line Candle", "signal_type": "bullish/bearish", "candles": 1},
    "CDLSPINNINGTOP" : {"name" : "Spinning Top", "signal_type": "bullish/bearish", "candles": 1},
    "CDLSTALLEDPATTERN" : {"name" : "Stalled Pattern", "signal_type": "bullish/bearish", "candles": 3},
    "CDLSTICKSANDWICH" : {"name" : "Stick Sandwich", "signal_type": "bullish", "candles": 3},
    "CDLTAKURI" : {"name" : "Takuri", "signal_type": "bullish", "candles": 1},
    "CDLTASUKIGAP" : {"name" : "Tasuki Gap", "signal_type": "bullish", "candles": 3},
    "CDLTHRUSTING" : {"name" : "Thrusting Pattern", "signal_type": "bearish", "candles": 2},
    "CDLTRISTAR" : {"name" : "Tristar Pattern", "signal_type": "bullish", "candles": 3},
    "CDLUNIQUE3RIVER" : {"name" : "Unique 3 River", "signal_type": "bullish", "candles": 3},
    "CDLUPSIDEGAP2CROWS" : {"name" : "Upside Gap Two Crows", "signal_type": "bearish", "candles": 3},
    "CDLXSIDEGAP3METHODS" : {"name" : "Upside/Downside Gap / Three Methods", "signal_type": "bullish/bearish", "candles": 3},
}

"""
This evaluation result is based on the prices of more than 2000 NYSE symbols from Jan 2014 to Dec 2015.
The program counts how many times the price increase or decrease five days after the candlestick patterns
occurred. Based on the result, we can see that there are a group of patterns that can accurately predict
the trend in five days.

Pattern      Gain  Lose
CDLTAKURI :  1.0   0.0
CDLEVENINGDOJISTAR :  0.0   1.0
CDLMATCHINGLOW :  1.0   0.0
CDLABANDONEDBABY :  0.375   0.625
CDLDOJISTAR :  0.516959377933   0.483040622067
CDL3WHITESOLDIERS :  1.0   0.0
CDLKICKINGBYLENGTH :  0.375   0.625
CDLHIGHWAVE :  0.564672299612   0.435327700388
CDLHARAMI :  0.522334623871   0.477665376129
CDLBREAKAWAY :  0.596774193548   0.403225806452
CDLSPINNINGTOP :  0.544268140003   0.455731859997
CDLHOMINGPIGEON :  1.0   0.0
CDL3STARSINSOUTH :  nan   nan
CDLBELTHOLD :  0.497133287361   0.502866712639
CDL3LINESTRIKE :  0.504918032787   0.495081967213
CDLCOUNTERATTACK :  0.502732240437   0.497267759563
CDLRICKSHAWMAN :  1.0   0.0
CDLENGULFING :  0.499394044321   0.500605955679
CDLHIKKAKE :  0.470770050626   0.529229949374
CDLTHRUSTING :  0.0   1.0
CDLHANGINGMAN :  0.0   1.0
CDLUPSIDEGAP2CROWS :  0.0   1.0
CDLUNIQUE3RIVER :  1.0   0.0
CDLDOJI :  1.0   0.0
CDLCONCEALBABYSWALL :  nan   nan
CDLEVENINGSTAR :  0.0   1.0
CDLLADDERBOTTOM :  1.0   0.0
CDLMORNINGSTAR :  1.0   0.0
CDLGRAVESTONEDOJI :  1.0   0.0
CDLIDENTICAL3CROWS :  0.0   1.0
CDLLONGLEGGEDDOJI :  1.0   0.0
CDLCLOSINGMARUBOZU :  0.554919571955   0.445080428045
CDLONNECK :  0.0   1.0
CDLHAMMER :  1.0   0.0
CDLMARUBOZU :  0.544496566728   0.455503433272
CDL2CROWS :  0.0   1.0
CDL3INSIDE :  0.530993431856   0.469006568144
CDLINVERTEDHAMMER :  1.0   0.0
CDLDARKCLOUDCOVER :  0.0   1.0
CDL3BLACKCROWS :  0.0   1.0
CDLSHOOTINGSTAR :  0.0   1.0
CDLSTALLEDPATTERN :  0.0   1.0
CDLPIERCING :  1.0   0.0
CDLHIKKAKEMOD :  0.44930417495   0.55069582505
CDLGAPSIDESIDEWHITE :  0.771428571429   0.228571428571
CDLTASUKIGAP :  0.539103232534   0.460896767466
CDLLONGLINE :  0.523644004866   0.476355995134
CDLMORNINGDOJISTAR :  1.0   0.0
CDLSEPARATINGLINES :  0.484116022099   0.515883977901
CDLINNECK :  0.0   1.0
CDLSHORTLINE :  0.527140663466   0.472859336534
CDLXSIDEGAP3METHODS :  0.493413624388   0.506586375612
CDLDRAGONFLYDOJI :  1.0   0.0
CDLHARAMICROSS :  0.516694172908   0.483305827092
CDLSTICKSANDWICH :  1.0   0.0
CDL3OUTSIDE :  0.511015535855   0.488984464145
CDLTRISTAR :  0.476293103448   0.523706896552
CDLMATHOLD :  1.0   0.0
CDLRISEFALL3METHODS :  0.505882352941   0.494117647059
CDLADVANCEBLOCK :  0.0   1.0
CDLKICKING :  0.428571428571   0.571428571429

---------------------------------------------
Pattern   Gain Percent  Lose Percent   Instances
CDLTAKURI :  1.0   0.0   5178.0
CDLEVENINGDOJISTAR :  0.0   1.0   502.0
CDLMATCHINGLOW :  1.0   0.0   5300.0
CDL3WHITESOLDIERS :  1.0   0.0   207.0
CDLHOMINGPIGEON :  1.0   0.0   3896.0
CDLRICKSHAWMAN :  1.0   0.0   35336.0
CDLTHRUSTING :  0.0   1.0   1755.0
CDLHANGINGMAN :  0.0   1.0   5985.0
CDLUPSIDEGAP2CROWS :  0.0   1.0   96.0
CDLUNIQUE3RIVER :  1.0   0.0   512.0
CDLDOJI :  1.0   0.0   48433.0
CDLEVENINGSTAR :  0.0   1.0   1496.0
CDLLADDERBOTTOM :  1.0   0.0   404.0
CDLMORNINGSTAR :  1.0   0.0   1838.0
CDLGRAVESTONEDOJI :  1.0   0.0   4354.0
CDLIDENTICAL3CROWS :  0.0   1.0   26.0
CDLLONGLEGGEDDOJI :  1.0   0.0   48361.0
CDLONNECK :  0.0   1.0   661.0
CDLHAMMER :  1.0   0.0   6938.0
CDL2CROWS :  0.0   1.0   199.0
CDLINVERTEDHAMMER :  1.0   0.0   4946.0
CDLDARKCLOUDCOVER :  0.0   1.0   1057.0
CDL3BLACKCROWS :  0.0   1.0   31.0
CDLSHOOTINGSTAR :  0.0   1.0   3679.0
CDLSTALLEDPATTERN :  0.0   1.0   775.0
CDLPIERCING :  1.0   0.0   907.0
CDLMORNINGDOJISTAR :  1.0   0.0   644.0
CDLINNECK :  0.0   1.0   372.0
CDLDRAGONFLYDOJI :  1.0   0.0   5251.0
CDLSTICKSANDWICH :  1.0   0.0   430.0
CDLMATHOLD :  1.0   0.0   5.0
CDLADVANCEBLOCK :  0.0   1.0   2064.0
"""

GOOD_PATTERNS = [
"CDLTAKURI",
"CDLEVENINGDOJISTAR",
"CDLMATCHINGLOW",
"CDL3WHITESOLDIERS",
"CDLHOMINGPIGEON",
"CDLRICKSHAWMAN",
"CDLTHRUSTING",
"CDLHANGINGMAN",
"CDLUPSIDEGAP2CROWS",
"CDLUNIQUE3RIVER",
"CDLDOJI",
"CDLEVENINGSTAR",
"CDLLADDERBOTTOM",
"CDLMORNINGSTAR",
"CDLGRAVESTONEDOJI",
"CDLIDENTICAL3CROWS",
"CDLLONGLEGGEDDOJI",
"CDLONNECK",
"CDLHAMMER",
"CDL2CROWS",
"CDLINVERTEDHAMMER",
"CDLDARKCLOUDCOVER",
"CDL3BLACKCROWS",
"CDLSHOOTINGSTAR",
"CDLSTALLEDPATTERN",
"CDLPIERCING",
"CDLMORNINGDOJISTAR",
"CDLINNECK",
"CDLDRAGONFLYDOJI",
"CDLSTICKSANDWICH",
"CDLMATHOLD",
"CDLADVANCEBLOCK"
]

def analyze_pattern(pattern_name, open, high, low, close):
    """
    Analyze the specified candlestick pattern.

    Parameters
    ----------
    pattern_name: String
        the name of the pattern, defined as the keys of PATTERNS
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray

    Returns
    ---------
    result: np.ndarray
    """
    result = getattr(talib, pattern_name)(open, high, low, close)
    return result


def candlestick_patterns(prices, pattern_names=GOOD_PATTERNS):
    signals = pd.DataFrame(index=prices.index)
    open = prices["Open"].values
    high = prices["High"].values
    low = prices["Low"].values
    close = prices["Close"].values
    for name in pattern_names:
        result = analyze_pattern(name, open, high, low, close)
        result = pd.DataFrame(result, index=prices.index, columns=[name])
        signals = signals.join(result)

    return signals


