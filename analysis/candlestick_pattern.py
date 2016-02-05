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
This evaluation result is based on the prices of more than 5600 symbols from Jan 2014 to Jan 2016.
The program counts how many times the price increase or decrease five days after the candlestick patterns
occurred.

- start date: 2014-01-01
- end date: 2016-01-29
- symbols: about 5,600 symbols
- csv files: https://dl.dropboxusercontent.com/u/10880933/prices.zip

PATTERN :  BULL_PERCENT  BULL_SIGNAL_COUNT  BEAR_PERCENT  BEAR_SIGNAL_COUNT
CDLTAKURI :  0.448715456637   61734.0   nan   0.0
CDLEVENINGDOJISTAR :  nan   0.0   0.474894934749   4521.0
CDLMATCHINGLOW :  0.48021896493   49871.0   nan   0.0
CDLABANDONEDBABY :  0.365384615385   156.0   0.436781609195   174.0
CDLDOJISTAR :  0.511126031076   31278.0   0.51518718326   30585.0
CDL3WHITESOLDIERS :  0.433591423466   1679.0   nan   0.0
CDLKICKINGBYLENGTH :  0.458333333333   120.0   0.402684563758   149.0
CDLHIGHWAVE :  0.479077000251   199350.0   0.50177899242   135751.0
CDLHARAMI :  0.491009765428   99330.0   0.515640822436   90852.0
CDLBREAKAWAY :  0.530120481928   166.0   0.523178807947   151.0
CDLSPINNINGTOP :  0.479935768133   303899.0   0.501488119775   242588.0
CDLHOMINGPIGEON :  0.492765070138   31652.0   nan   0.0
CDL3STARSINSOUTH :  0.5   14.0   nan   0.0
CDLBELTHOLD :  0.455146911853   250150.0   0.495985766707   269790.0
CDL3LINESTRIKE :  0.46686746988   1328.0   0.537959183673   1225.0
CDLCOUNTERATTACK :  0.477540106952   1870.0   0.491997934951   1937.0
CDLRICKSHAWMAN :  0.481537013008   252776.0   nan   0.0
CDLENGULFING :  0.466071864218   86079.0   0.484897275107   106206.0
CDLHIKKAKE :  0.474671404112   155358.0   0.51083996078   156043.0
CDLTHRUSTING :  nan   0.0   0.482123647409   15803.0
CDLHANGINGMAN :  nan   0.0   0.530684415566   69563.0
CDLUPSIDEGAP2CROWS :  nan   0.0   0.51724137931   725.0
CDLUNIQUE3RIVER :  0.483233688589   3847.0   nan   0.0
CDLDOJI :  0.477345860037   448748.0   nan   0.0
CDLCONCEALBABYSWALL :  0.470588235294   17.0   nan   0.0
CDLEVENINGSTAR :  nan   0.0   0.473111834218   11678.0
CDLLADDERBOTTOM :  0.446574369897   2817.0   nan   0.0
CDLMORNINGSTAR :  0.478154187114   12634.0   nan   0.0
CDLGRAVESTONEDOJI :  0.495953677772   58201.0   nan   0.0
CDLIDENTICAL3CROWS :  nan   0.0   0.449019607843   510.0
CDLLONGLEGGEDDOJI :  0.479824951603   402403.0   nan   0.0
CDLCLOSINGMARUBOZU :  0.444134353674   202808.0   0.463446178041   193304.0
CDLONNECK :  nan   0.0   0.458213256484   6593.0
CDLHAMMER :  0.464080367981   62612.0   nan   0.0
CDLMARUBOZU :  0.436259131448   89252.0   0.463584278675   87270.0
CDL2CROWS :  nan   0.0   0.504137931034   1450.0
CDL3INSIDE :  0.465725036811   18337.0   0.503379818525   16421.0
CDLINVERTEDHAMMER :  0.521574884011   54531.0   nan   0.0
CDLDARKCLOUDCOVER :  nan   0.0   0.462742175857   9394.0
CDL3BLACKCROWS :  nan   0.0   0.447191011236   445.0
CDLSHOOTINGSTAR :  nan   0.0   0.50070381433   29127.0
CDLSTALLEDPATTERN :  nan   0.0   0.537805571347   5277.0
CDLPIERCING :  0.474925047697   7338.0   nan   0.0
CDLHIKKAKEMOD :  0.490204808549   2246.0   0.531294792164   2093.0
CDLGAPSIDESIDEWHITE :  0.461691259932   7048.0   0.479610750695   4316.0
CDLTASUKIGAP :  0.527758007117   5620.0   0.494984434452   5782.0
CDLLONGLINE :  0.454098234843   260600.0   0.488878568543   264849.0
CDLMORNINGDOJISTAR :  0.459316517494   4916.0   nan   0.0
CDLSEPARATINGLINES :  0.452568823426   5703.0   0.487550665895   8635.0
CDLINNECK :  nan   0.0   0.475895316804   4356.0
CDLSHORTLINE :  0.468318663733   239952.0   0.506938245978   192700.0
CDLXSIDEGAP3METHODS :  0.509934695012   7197.0   0.511521323997   7855.0
CDLDRAGONFLYDOJI :  0.448458348796   61979.0   nan   0.0
CDLHARAMICROSS :  0.489010514187   34715.0   0.518490731189   31989.0
CDLSTICKSANDWICH :  0.505945639864   3532.0   nan   0.0
CDL3OUTSIDE :  0.480983149626   39465.0   0.491453251414   49317.0
CDLTRISTAR :  0.465455475947   3908.0   0.473670624677   3874.0
CDLMATHOLD :  0.363636363636   33.0   nan   0.0
CDLRISEFALL3METHODS :  0.54358974359   195.0   0.437275985663   279.0
CDLADVANCEBLOCK :  nan   0.0   0.535942848638   13438.0
CDLKICKING :  0.416666666667   120.0   0.362416107383   149.0
"""

GOOD_PATTERNS = ["CDLBREAKAWAY", "CDLHANGINGMAN", "CDLINVERTEDHAMMER", "CDLSTALLEDPATTERN", "CDLADVANCEBLOCK"]


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


