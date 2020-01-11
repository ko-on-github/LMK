
import matplotlib
from lmk.ticker import Ticker

matplotlib.rcParams['figure.figsize'] = (19, 8)

ticker = Ticker("^GSPC")
ticker.retrieve_history("1990-01-01", "2020-1-5", "M") # Start date "yyyy-mm-dd", end date, frequency ("D", "W", "M")
ticker.visualize("V,C,CL,LMK,WM,PV")

# To run, in terminal python main.py when you are in LMK folder
# To run spyder, in terminal spyder main.py when you are in LMK folder

# Experiment 2
