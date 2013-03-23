import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import numpy as np
import datetime as dt


def simulate(closing_prices, allocations):

    na_allocated_port = closing_prices.copy() * allocations
    na_daily_returns = na_allocated_port.sum(axis=1)

    cumulative_return = na_daily_returns[-1]
    tsu.returnize0(na_daily_returns)
    standard_deviation = np.std(na_daily_returns)
    average_daily_returns = np.average(na_daily_returns)
    sharpe_ratio = (average_daily_returns / standard_deviation *
                    np.sqrt(len(na_daily_returns)))

    return (standard_deviation,
            average_daily_returns,
            sharpe_ratio,
            cumulative_return)


def allAllocations():
    a_poss_allottments = [.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.]
    combinations = []
    for i in a_poss_allottments:
        for j in a_poss_allottments:
            for k in a_poss_allottments:
                for l in a_poss_allottments:
                    if i + j + k + l == 1:
                        combinations.append([i, j, k, l])
    return combinations


def main():
    symbols = ['GOOG', 'DIS', 'MSFT', 'AAPL']
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2011, 12, 31)

    hours = dt.timedelta(hours=16)
    open_market_days = du.getNYSEdays(start_date, end_date, hours)
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    file_columns = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    file_data = c_dataobj.get_data(open_market_days, symbols, file_columns)
    stock_data = dict(zip(file_columns, file_data))
    closing_prices = stock_data['close'].values
    na_closing_prices = (closing_prices / closing_prices[0, :])

    best_contender = [0, 0, 0, 0]
    best_allocation = ""
    for a in allAllocations():
        allocation_test = simulate(na_closing_prices, a)
        if allocation_test[2] > best_contender[2]:
            best_contender = allocation_test
            best_allocation = a

    print "Start Date: " + str(start_date)
    print "End Date: " + str(end_date)
    print "Symbols: " + str(symbols)
    print "Optimal Allocations: " + str(best_allocation)
    print "Sharpe Ratio: " + str(best_contender[2])
    print "Volatility (stdev of daily returns): " + str(best_contender[0])
    print "Average Daily Return: " + str(best_contender[1])
    print "Cumulative Return: " + str(best_contender[3])

if __name__ == '__main__':
    main()
