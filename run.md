```python
>>> # http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-matplotlib
... %matplotlib inline
...
>>> # http://matplotlib.org/users/customizing.html
... import matplotlib
>>> matplotlib.rcParams['figure.figsize'] = (19, 8)
>>> # matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
...
... # http://stackoverflow.com/questions/11707586/python-pandas-widen-output-display
... import pandas
>>> pandas.set_option('display.max_columns', 500)
>>> pandas.set_option('display.width', 200)
```

```python
>>> import logging
>>> from datetime import timedelta
...
>>> import lmk.ticker
>>> #from imp import reload
... #reload(lmk.calculator.LMKBandCalculator)
... #reload(lmk.ticker)
...
... from lmk.ticker import Ticker
>>> from lmk.utils import env
>>> env.logger.setLevel(logging.DEBUG)
```

```python
>>> stk = Ticker("TSLA")
...
>>> end = env._today
>>> end = (env.today - timedelta(1)).strftime("%Y-%m-%d")
>>> stk.retrieve_history("2016-02-01", end)
>>> #stk.preprocess_history(freq="W-MON")
... stk.preprocess_history(freq="D")
...
>>> #h = stk.history
... #print(h.tail(2))
...
... stk.visualize("V,C,HLC,BAND,WM,PV,PVL,EE,ODR", ylimits=(140,300))
```

```python
>>> stk = Ticker("000001.SS")
...
>>> stk.retrieve_history("2015-02-01", "2015-12-01")
>>> stk.preprocess_history(freq="D")
...
>>> stk.visualize("V,C,HLC,BAND,WM,PVL,EE,ODR", ylimits=(2500,5200))
```