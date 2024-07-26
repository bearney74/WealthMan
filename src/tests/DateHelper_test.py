import unittest
from datetime import date

from libs.DateHelper import DateHelper
from libs.EnumTypes import AccountType, AccountOwnerType


class DateHelperTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_days_in_year(self):
        _dt = DateHelper(None, None)
        self.assertEqual(_dt.days_in_year(), 365.0)
        
        _dt = DateHelper(begin_dt=date(2000, 1, 1), end_dt=date(2000, 12, 31))
        self.assertEqual(_dt.days_in_year(), 366.0)
        
        _dt = DateHelper(None, end_dt=date(2001, 12, 31))
        self.assertEqual(_dt.days_in_year(), 365.0)
        
        _dt = DateHelper(begin_dt=date(2002, 1, 1), end_dt=None)
        self.assertEqual(_dt.days_in_year(), 365.0)
        
        _dt = DateHelper(begin_dt=date(2003, 9, 1), end_dt=date(2003, 9, 30))
        self.assertEqual(_dt.days_in_year(), 30)
        
    def test_percent_of_year(self):
        _dt = DateHelper(None, None)
        self.assertEqual(_dt.percent_of_year(), 100.0)
        
        _dt = DateHelper(begin_dt=date(2000, 1, 1), end_dt=date(2000, 12, 31))
        self.assertEqual(_dt.percent_of_year(), 100.0)
        
        _dt = DateHelper(None, end_dt=date(2001, 12, 31))
        self.assertEqual(_dt.percent_of_year(), 100.0)
        
        _dt = DateHelper(begin_dt=date(2002, 1, 1), end_dt=None)
        self.assertEqual(_dt.percent_of_year(), 100.0)
        
        _dt = DateHelper(begin_dt=date(2003, 9, 1), end_dt=date(2003, 9, 30))
        self.assertEqual(_dt.percent_of_year(), 100.0 * 30/365.0)
        


if __name__ == "__main__":
    unittest.main()
