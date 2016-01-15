import pandas as pd
import talib

# TODO modify the data of other patterns

PATTERNS = {
    "CDL2CROWS" : {"name" : "Two Crows", "signal_type": "bearish", "candles": 2},
    "CDL3BLACKCROWS" : {"name" : "Three Black Crows", "signal_type": "bearish", "candles": 3},
    "CDL3INSIDE" : {"name" : "Three Inside Up/Down", "signal_type": "bullish/bearish", "candles": 3},
    # "CDL3LINESTRIKE" : {"name" : "Three-Line Strike", "signal_type": "bullish", "candles": 1},
    # "CDL3OUTSIDE" : {"name" : "Three Outside Up/Down", "signal_type": "bullish", "candles": 1},
    # "CDL3STARSINSOUTH" : {"name" : "Three Stars In The South", "signal_type": "bullish", "candles": 1},
    "CDL3WHITESOLDIERS" : {"name" : "Three Advancing White Soldiers", "signal_type": "bullish", "candles": 3},
    "CDLABANDONEDBABY" : {"name" : "Abandoned Baby", "signal_type": "bullish", "candles": 3},
    # "CDLADVANCEBLOCK" : {"name" : "Advance Block", "signal_type": "bullish", "candles": 1},
    # "CDLBELTHOLD" : {"name" : "Belt-hold", "signal_type": "bullish", "candles": 1},
    # "CDLBREAKAWAY" : {"name" : "Breakaway", "signal_type": "bullish", "candles": 1},
    # "CDLCLOSINGMARUBOZU" : {"name" : "Closing Marubozu", "signal_type": "bullish", "candles": 1},
    # "CDLCONCEALBABYSWALL" : {"name" : "Concealing Baby Swallow", "signal_type": "bullish", "candles": 1},
    # "CDLCOUNTERATTACK" : {"name" : "Counterattack", "signal_type": "bullish", "candles": 1},
    "CDLDARKCLOUDCOVER" : {"name" : "Dark Cloud Cover", "signal_type": "bearish", "candles": 2},
    # "CDLDOJI" : {"name" : "Doji", "signal_type": "bullish", "candles": 1},
    # "CDLDOJISTAR" : {"name" : "Doji Star", "signal_type": "bullish", "candles": 1},
    # "CDLDRAGONFLYDOJI" : {"name" : "Dragonfly Doji", "signal_type": "bullish", "candles": 1},
    "CDLENGULFING" : {"name" : "Engulfing Pattern", "signal_type": "bullish/bearish", "candles": 2},
    # "CDLEVENINGDOJISTAR" : {"name" : "Evening Doji Star", "signal_type": "bullish", "candles": 1},
    "CDLEVENINGSTAR" : {"name" : "Evening Star", "signal_type": "bearish", "candles": 3},
    # "CDLGAPSIDESIDEWHITE" : {"name" : "Up/Down-gap side-by-side white lines", "signal_type": "bullish", "candles": 1},
    # "CDLGRAVESTONEDOJI" : {"name" : "Gravestone Doji", "signal_type": "bullish", "candles": 1},
    "CDLHAMMER" : {"name" : "Hammer", "signal_type": "bullish", "candles": 1},
    "CDLHANGINGMAN" : {"name" : "Hanging Man", "signal_type": "bearish", "candles": 1},
    # "CDLHARAMI" : {"name" : "Harami Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLHARAMICROSS" : {"name" : "Harami Cross Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLHIGHWAVE" : {"name" : "High-Wave Candle", "signal_type": "bullish", "candles": 1},
    # "CDLHIKKAKE" : {"name" : "Hikkake Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLHIKKAKEMOD" : {"name" : "Modified Hikkake Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLHOMINGPIGEON" : {"name" : "Homing Pigeon", "signal_type": "bullish", "candles": 1},
    # "CDLIDENTICAL3CROWS" : {"name" : "Identical Three Crows", "signal_type": "bullish", "candles": 1},
    # "CDLINNECK" : {"name" : "In-Neck Pattern", "signal_type": "bullish", "candles": 1},
    "CDLINVERTEDHAMMER" : {"name" : "Inverted Hammer", "signal_type": "bullish", "candles": 1},
    # "CDLKICKING" : {"name" : "Kicking", "signal_type": "bullish", "candles": 1},
    # "CDLKICKINGBYLENGTH" : {"name" : "Kicking - bull/bear determined by the longer marubozu", "signal_type": "bullish", "candles": 1},
    # "CDLLADDERBOTTOM" : {"name" : "Ladder Bottom", "signal_type": "bullish", "candles": 1},
    # "CDLLONGLEGGEDDOJI" : {"name" : "Long Legged Doji", "signal_type": "bullish", "candles": 1},
    # "CDLLONGLINE" : {"name" : "Long Line Candle", "signal_type": "bullish", "candles": 1},
    # "CDLMARUBOZU" : {"name" : "Marubozu", "signal_type": "bullish", "candles": 1},
    # "CDLMATCHINGLOW" : {"name" : "Matching Low", "signal_type": "bullish", "candles": 1},
    # "CDLMATHOLD" : {"name" : "Mat Hold", "signal_type": "bullish", "candles": 1},
    # "CDLMORNINGDOJISTAR" : {"name" : "Morning Doji Star", "signal_type": "bullish", "candles": 1},
    "CDLMORNINGSTAR" : {"name" : "Morning Star", "signal_type": "bullish", "candles": 3},
    # "CDLONNECK" : {"name" : "On-Neck Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLPIERCING" : {"name" : "Piercing Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLRICKSHAWMAN" : {"name" : "Rickshaw Man", "signal_type": "bullish", "candles": 1},
    # "CDLRISEFALL3METHODS" : {"name" : "Rising/Falling Three Methods", "signal_type": "bullish", "candles": 1},
    # "CDLSEPARATINGLINES" : {"name" : "Separating Lines", "signal_type": "bullish", "candles": 1},
    "CDLSHOOTINGSTAR" : {"name" : "Shooting Star", "signal_type": "bearish", "candles": 1},
    # "CDLSHORTLINE" : {"name" : "Short Line Candle", "signal_type": "bullish", "candles": 1},
    # "CDLSPINNINGTOP" : {"name" : "Spinning Top", "signal_type": "bullish", "candles": 1},
    # "CDLSTALLEDPATTERN" : {"name" : "Stalled Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLSTICKSANDWICH" : {"name" : "Stick Sandwich", "signal_type": "bullish", "candles": 1},
    # "CDLTAKURI" : {"name" : "Takuri", "signal_type": "bullish", "candles": 1},
    # "CDLTASUKIGAP" : {"name" : "Tasuki Gap", "signal_type": "bullish", "candles": 1},
    # "CDLTHRUSTING" : {"name" : "Thrusting Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLTRISTAR" : {"name" : "Tristar Pattern", "signal_type": "bullish", "candles": 1},
    # "CDLUNIQUE3RIVER" : {"name" : "Unique 3 River", "signal_type": "bullish", "candles": 1},
    # "CDLUPSIDEGAP2CROWS" : {"name" : "Upside Gap Two Crows", "signal_type": "bullish", "candles": 1},
    # "CDLXSIDEGAP3METHODS" : {"name" : "Upside/Downside Gap Three Methods", "signal_type": "bullish", "candles": 1},
}


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


