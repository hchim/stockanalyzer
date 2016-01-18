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
occurred.

CDLTAKURI :  0.516863818555   10229.0   nan   0.0
CDLEVENINGDOJISTAR :  nan   0.0   0.435402684564   1192.0
CDLMATCHINGLOW :  0.508389261745   10728.0   nan   0.0
CDL3WHITESOLDIERS :  0.509803921569   408.0   nan   0.0
CDLHOMINGPIGEON :  0.519201228879   7812.0   nan   0.0
CDLRICKSHAWMAN :  0.504142160629   71581.0   nan   0.0
CDLTHRUSTING :  nan   0.0   0.449184441656   3985.0
CDLHANGINGMAN :  nan   0.0   0.477458700015   12954.0
CDLUPSIDEGAP2CROWS :  nan   0.0   0.50495049505   202.0
CDLUNIQUE3RIVER :  0.513339466421   1087.0   nan   0.0
CDLDOJI :  0.508722126224   97224.0   nan   0.0
CDLEVENINGSTAR :  nan   0.0   0.451985773563   3374.0
CDLLADDERBOTTOM :  0.439790575916   955.0   nan   0.0
CDLMORNINGSTAR :  0.514404432133   3610.0   nan   0.0
CDLGRAVESTONEDOJI :  0.512814592473   8662.0   nan   0.0
CDLIDENTICAL3CROWS :  nan   0.0   0.309523809524   84.0
CDLLONGLEGGEDDOJI :  0.50895000979   97039.0   nan   0.0
CDLONNECK :  nan   0.0   0.446451612903   1550.0
CDLHAMMER :  0.502481917459   14102.0   nan   0.0
CDL2CROWS :  nan   0.0   0.479905437352   423.0
CDLINVERTEDHAMMER :  0.537686844058   9433.0   nan   0.0
CDLDARKCLOUDCOVER :  nan   0.0   0.448391140827   2393.0
CDL3BLACKCROWS :  nan   0.0   0.352941176471   85.0
CDLSHOOTINGSTAR :  nan   0.0   0.496181195681   7594.0
CDLSTALLEDPATTERN :  nan   0.0   0.503505417463   1569.0
CDLPIERCING :  0.510067114094   1788.0   nan   0.0
CDLMORNINGDOJISTAR :  0.496551724138   1305.0   nan   0.0
CDLINNECK :  nan   0.0   0.449122807018   855.0
CDLDRAGONFLYDOJI :  0.516975308642   10368.0   nan   0.0
CDLSTICKSANDWICH :  0.511085180863   857.0   nan   0.0
CDLMATHOLD :  0.4375   16.0   nan   0.0
CDLADVANCEBLOCK :  nan   0.0   0.507473481196   4148.0
"""


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


def candlestick_patterns(prices, pattern_names=[]):
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


