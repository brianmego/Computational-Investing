import datetime as dt
from nose.tools import istest
import assignment_1 as a


class TestAssignmentOne(object):

    @istest
    def Ex_1(self):
        target = a.simulate(dt.datetime(2010, 1, 1),
                            dt.datetime(2010, 12, 31),
                            ['AXP', 'HPQ', 'IBM', 'HNZ'],
                            [0.0, 0.0, 0.0, 1.0])
        expected = (0.0101467067654,
                    0.000657261102001,
                    1.02828403099,
                    1.16487261965)
        assert expected == target

    @istest
    def Ex_2(self):
        target = a.simulate(dt.datetime(2011, 1, 1),
                            dt.datetime(2011, 12, 31),
                            ['AAPL', 'GLD', 'GOOG', 'XOM'],
                            [0.4, 0.4, 0.0, 0.2])
        expected = (0.00924299255937,
                    0.000756285585593,
                    1.29889334008,
                    1.1960583568)
        assert expected == target
