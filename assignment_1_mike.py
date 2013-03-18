import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def main():
    stock_symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocations = [0.0, 0.0, 0.0, 1.0]
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    

    vol, daily_ret, sharpe, cum_ret = simulate(start_date, end_date, stock_symbols, allocations)

    print "\n\n\n"
    print "Start Date: %s %d, %d" % (start_date.strftime("%B"), start_date.day, start_date.year)
    print "End Date: %s %d, %d" % (end_date.strftime("%B"), end_date.day, end_date.year)
    print "Symbols: %s" % stock_symbols
    print "Optimal Allocations: %s" % allocations
    print "Sharp Ratio: %s" % sharpe
    print "Volatility: %s" % vol
    print "Average Daily Return: %s" % daily_ret
    print "Cumulative Return: %s" % cum_ret
    print "\n\n\n"

def simulate(start_date, end_date, stock_symbols, allocations):
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    ldf_data = c_dataobj.get_data(ldt_timestamps, stock_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    na_price = d_data['close'].values
    normalized_price = (na_price / na_price[0, :])
    norm_price = normalized_price.copy()
    stock_results = np.array(normalized_price)

    tsu.returnize0(norm_price)
    average = np.mean(norm_price)
    volatility = np.std(norm_price)
    sharpe_ratio = math.sqrt(252) * (average/volatility)
    cumulative = np.sum(stock_results[-1] * allocations)

    return volatility, average, sharpe_ratio, cumulative


main()