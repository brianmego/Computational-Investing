import argparse
import datetime as dt
import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da


def main(cash, orders, output_path):
    order_array = create_order_array(orders)

    symbols = ['GOOG', 'IBM', 'XOM', 'AAPL', '$SPX']
    start_date = dt.datetime(2011, 1, 14)
    end_date = dt.datetime(2011, 12, 15)

    hours = dt.timedelta(hours=16)
    open_market_days = du.getNYSEdays(start_date, end_date, hours)
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    file_columns = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    file_data = c_dataobj.get_data(open_market_days, symbols, file_columns)
    stock_data = dict(zip(file_columns, file_data))
    closing_prices = stock_data['close'].values
    na_closing_prices = (closing_prices / closing_prices[0,:])

    cash = int(cash)
    portfolioHoldings = {'GOOG': 0, 'IBM': 0, 'XOM': 0, 'AAPL': 0, '$SPX': 0, 'cash': cash}
    portfolioValues = np.zeros((len(open_market_days), len(symbols) + 1))
    for day in open_market_days:
        close_index = open_market_days.index(day)

        for order in order_array:
            date = order[0]
            symbol = order[1]
            orderType = order[2]
            shares = int(order[3])
            if day == date:
                symbol_index = symbols.index(symbol)
                stock_price = closing_prices[close_index][symbol_index]
                if symbol not in portfolioHoldings:
                        portfolioHoldings[symbol] = 0

                if orderType == 'Buy':
                    # print 'Buying ' + str(shares) + ' shares of ' + symbol + ' at ' + str(stock_price)
                    portfolioHoldings[symbol] += shares
                    cash -= (stock_price * shares)
                elif orderType == 'Sell':
                    # print 'Selling ' + str(shares) + ' shares of ' + symbol + ' at ' + str(stock_price)
                    portfolioHoldings[symbol] -= shares
                    cash += (stock_price * shares)
                else:
                    raise Exception('Bad Order Type')

        for symbol in symbols:
            symbol_index = symbols.index(symbol)
            portfolioValues[close_index][symbol_index] = closing_prices[
                close_index][symbol_index] * (float(portfolioHoldings[symbol]))

        portfolioValues[close_index][5] = cash

    total_return = np.sum(portfolioValues[-1]) / np.sum(portfolioValues[0])
    na_daily_returns = (portfolioValues.copy()).sum(axis=1)
    tsu.returnize0(na_daily_returns)
    standard_deviation = np.std(na_daily_returns)
    average_daily_returns = np.average(na_daily_returns)
    sharpe_ratio = (average_daily_returns / standard_deviation *
                    np.sqrt(252))

    benchmarkPortfolio = na_closing_prices[:, symbols.index('$SPX')]
    na_benchmark_daily_returns = benchmarkPortfolio.copy()
    tsu.returnize0(na_benchmark_daily_returns)
    benchmark_total_return = benchmarkPortfolio[-1] / benchmarkPortfolio[0]
    benchmark_standard_deviation = np.std(na_benchmark_daily_returns)
    benchmark_average_daily_returns = np.average(na_benchmark_daily_returns)
    benchmark_sharpe_ratio = (benchmark_average_daily_returns / benchmark_standard_deviation *
                              np.sqrt(252))

    print 'The final value of the portfolio using the sample file is -- ' + str(end_date) + ', ' + str(np.sum(portfolioValues[-1]))
    print ''
    print 'Details of the Performance of the portfolio :'
    print ''
    print 'Data Range : ' + str(open_market_days[0]) + ' to ' + str(open_market_days[-1])
    print ''
    print 'Sharpe Ratio of Fund : ' + str(sharpe_ratio)
    print 'Sharp Ratio of $SPX : ' + str(benchmark_sharpe_ratio)
    print ''
    print 'Total Return of Fund : ' + str(total_return)
    print 'Total Return of $SPX : ' + str(benchmark_total_return)
    print ''
    print 'Standard Deviation of Fund : ' + str(standard_deviation)
    print 'Standard Deviation of $SPX : ' + str(benchmark_standard_deviation)
    print ''
    print 'Average Daily Return of Fund : ' + str(average_daily_returns)
    print 'Average Daily Return of $SPX : ' + str(benchmark_average_daily_returns)


def create_order_array(orders_file):
    order_array = []
    dtype = [('year', int), ('month', int), ('day', int), ('symbol', 'S10'), ('order', 'S10'), ('shares', int)]
    na_data = np.loadtxt(orders_file, delimiter=',', dtype=dtype)
    # na_dates = na_data[:1]
    # na_orders = np.str(na_data[:, 3:6])
    na_data = np.sort(na_data, order=['year', 'month', 'day'])
    raw_input(na_data)
    with open(orders, 'r') as f:
        contents = f.read()
        allOrders = contents.splitlines()
        for order in allOrders:
            pieces = order.split(',')
            date = dt.datetime(int(pieces[0]), int(pieces[1]), int(pieces[2]), 16)
            symbol = pieces[3]
            orderType = pieces[4]
            shares = pieces[5]
            order_array.append([date, symbol, orderType, shares])
    return np.array(order_array)


def report_output():
    print '\n\n'
    print 'The final value of the portfolio using the sample file is -- 2011,12,20,1133860'
    print ''
    print 'Details of the Performance of the portfolio :'
    print ''
    print 'Data Range : 2011-01-10 16:00:00 to 2011-12-20 16:00:00'
    print ''
    print 'Sharpe Ratio of Fund : 1.21540462111'
    print 'Sharp Ratio of $SPX : 0.018339141227'
    print ''
    print 'Total Return of Fund : 1.13386'
    print 'Total Return of $SPX : 0.97759401457'
    print ''
    print 'Standard Deviation of Fund : 0.00717514512699'
    print 'Standard Deviation of $SPX : 0.0149090969828'
    print ''
    print 'Average Daily Return of Fund : 0.000549352749569'
    print 'Average Daily Return of $SPX : 1.72238432443e-05'


def parse_args():
    '''Defines command line arguments and parses them into variables'''

    parser = argparse.ArgumentParser(
        description="Runs script for given school and semester")
    parser.add_argument('cash', help="Starting Portfolio Amount")
    parser.add_argument('orders_file', help="CSV with orders")
    parser.add_argument('values_file', help="Output Path")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    cash = args.cash
    orders = args.orders_file
    output_path = args.values_file

    # print symbols
    # print closing_prices[-1]
    # print open_market_days[5]
    # print closing_prices[5]
    main(cash, orders, output_path)
