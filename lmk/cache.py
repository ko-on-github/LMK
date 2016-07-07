import os
from os.path import join

from pandas import HDFStore, DataFrame, Series

from .utils import Singleton

TABLE_RANGE = "_cache_range"
TABLE_NAME = "_symbol_name"

@Singleton
class Cache:
    def __init__(self, cache_dir=".cache"):
        os.makedirs(cache_dir, exist_ok=True) # mkdir -p ...
        self.fn = join(cache_dir, "lmk.hd5")
        with HDFStore(self.fn) as cache:
            if TABLE_RANGE in cache:
                self.range = cache.get(TABLE_RANGE)
            else:
                self.range = DataFrame({"start": Series([], dtype="datetime64[ns]"),
                                        "end": Series([], dtype="datetime64[ns]")},)
                cache.put(TABLE_RANGE, self.range)

            if TABLE_NAME in cache:
                self.name = cache.get(TABLE_NAME)
            else:
                self.name = Series([])
                cache.put(TABLE_NAME, self.name)

    def get(self, symbol, start, end):
        _symbol = symbol.replace(".", "_")
        if symbol in self.range:
            _start, _end = self.range.loc[symbol]
            # cache hit - part of existing data.
            if _start <= start <= end <= _end:
                with HDFStore(self.fn) as cache:
                    h = self.cache.get(_symbol)
                    h = h.loc[start:end]

                    return h

    def put(self, symbol, history, start, end):
        # HDF5 table name better to be a valid variable name.
        # e.g. 000001.SS => t000001_SS; TSLA => tTSLA
        _symbol = "t{}".format(symbol).replace(".", "_")
        if symbol in self.range:
            _start, _end = self.range.loc[symbol]

            # 1. part of existing cache, nothing need to be done.
            if _start <= start <= end <= _end:
                return

            # 2. there is overlap
            elif _start > start and _end > end:
                with HDFStore(self.fn) as cache:
                    h = cache.get(_symbol)
                    h.loc[start: end] = history
                    self.range[symbol] = start, _end

                    cache.put(_symbol, h)
                    cache.put(TABLE_RANGE, self.range)

            # 3. no overlap, save the recent data.
            else:
                if _end < start: # new data is more recent.
                    self.range[symbol] = start, end

                    with HDFStore(self.fn) as cache:
                        cache.put(_symbol, h)
                        cache.put(TABLE_RANGE, self.range)

    def flush_name(self):
        with HDFStore(self.fn) as cache:
            cache.put(TABLE_NAME, self.name)
