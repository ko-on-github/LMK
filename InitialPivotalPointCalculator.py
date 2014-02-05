from collections import namedtuple

from constants import *

Extreme = namedtuple("Exteme", ["when", "value"])

class InitialPivotalPointCalculator(object):
    def __init__(self, atr_factor=2):
        # internal state
        self.trend = None
        self.last_price = None
        self.initialized = False
        self.done = False

        # OUT
        self.peak = None
        self.valley = None
        self.band = None # initial position
        self.atr_factor = atr_factor

    def __call__(self, tick):
        if self.done: return

        self.distance = tick["ATR"] * self.atr_factor
        current_price = Extreme(tick.name, tick["Close"])

        new_extreme = False
        if self.last_price:
            if current_price.value > self.last_price.value:
                if self.trend == TREND_DNWARD:
                    new_extreme = True
                self.trend = TREND_UPWARD
            if  current_price.value < self.last_price.value:
                if self.trend == TREND_UPWARD:
                    new_extreme = True
                self.trend = TREND_DNWARD

        if new_extreme:
            # initialize when we run cross first extremum, peak or valley
            if not self.initialized:
                self.initialized = True
                self.peak = self.last_price
                self.valley = self.last_price

            if self.trend == TREND_UPWARD: # new valley
                if self.last_price.value < self.valley.value:
                    self.valley = self.last_price
            elif self.trend == TREND_DNWARD: # new peak
                if self.last_price.value > self.peak.value:
                    self.peak = self.last_price

            if self.peak.value - self.valley.value >= self.distance:
                if self.peak.when > self.valley.when:
                    self.band = BAND_NAT_REACT
                else:
                    self.band = BAND_NAT_RALLY

                self.done = True

        # next round...
        self.last_price = current_price

if __name__ == "__main__":
    from datetime import datetime

    import matplotlib.pyplot as plt
    from pandas.io.data import DataReader
    import pandas as pd

    from ATRCalculator import ATRCalculator
    from common import show_plot

    history = DataReader("000001.SS", "yahoo", start="2008/1/1", end="2008/6/1")
    c = ATRCalculator(atr_period=14)
    history["ATR"] = history.apply(c, axis=1)
    c = InitialPivotalPointCalculator(atr_factor=2)
    history.apply(c, axis=1)

    plt.plot_date(history.index, history["Close"], "b")
    plt.axvline(pd.to_datetime(c.peak.when), color="g", alpha=.3)
    plt.axvline(pd.to_datetime(c.valley.when), color="r", alpha=.3)

    show_plot()


