import matplotlib
from lmk.ticker import Ticker

matplotlib.rcParams['figure.figsize'] = (19, 8)

ticker = Ticker("TSLA")
ticker.retrieve_history("2015-06-01", "2016-04-30")
ticker.visualize("V,C,CL,LMK,WM,PV")