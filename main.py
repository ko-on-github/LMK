import matplotlib
from lmk.ticker import Ticker

matplotlib.rcParams['figure.figsize'] = (19, 8)

ticker = Ticker("AAPL")
ticker.retrieve_history("2000-06-01", "2019-12-15", "M") # Start date "yyyy-mm-dd", end date, frequency ("D", "W", "M")
ticker.visualize("V,C,CL,LMK,WM,PV")

# To run, in terminal python main.py when you are in LMK folder