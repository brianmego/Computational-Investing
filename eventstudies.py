import numpy as np
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_actual_close = d_data['actual_close']
    # ts_market = df_actual_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_actual_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_actual_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_actual_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_actual_close[s_sym].ix[ldt_timestamps[i - 1]]
            with open('orders.csv', 'a') as f:
                if f_symprice_today < 5.0 and f_symprice_yest >= 5.0:
                    d = ldt_timestamps[i]
                    try:
                        d2 = ldt_timestamps[i+5]
                    except IndexError:
                        d2 = ldt_timestamps[-1]
                    f.write(str(d.year) + ',' + str(d.month) + ',' + str(d.day) + ',' + str(s_sym) + ',BUY,100\n')
                    f.write(str(d2.year) + ',' + str(d2.month) + ',' + str(d2.day) + ',' + str(s_sym) + ',SELL,100\n')
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    f = open('orders.csv', 'w')

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)
    print "Creating Study 1"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                     s_filename='2012Below5.pdf', b_market_neutral=True,
                     b_errorbars=True, s_market_sym='SPY')

    # ls_symbols = dataobj.get_symbols_from_list('sp5002008')
    # ls_symbols.append('SPY')
    # ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    # ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    # d_data = dict(zip(ls_keys, ldf_data))
    # for s_key in ls_keys:
    #     d_data[s_key] = d_data[s_key].fillna(method='ffill')
    #     d_data[s_key] = d_data[s_key].fillna(method='bfill')
    #     d_data[s_key] = d_data[s_key].fillna(1.0)

    # df_events = find_events(ls_symbols, d_data)
    # print "Creating Study 2"
    # ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
    #                  s_filename='2008Below5.pdf', b_market_neutral=True,
    #                  b_errorbars=True, s_market_sym='SPY')
