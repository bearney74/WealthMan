import unittest

from src.libs.Projections import DataItem
from src.libs.HistoricalAnalysis import (
    PeriodData,
    AllocationPeriod,
    AnnualReturnData,
    HistoricalData,
)


class HistoricalAnalysisTest(unittest.TestCase):
    def test_PeriodData(self):
        _pd = PeriodData(2000, 2010)

        self.assertTrue(isinstance(_pd.Period, DataItem))

        # Period
        self.assertEqual(str(_pd.Period), "2000-2010")
        self.assertEqual(_pd.Period.header, "Period")

        # EndingBalance
        _pd.EndingBalance.data = 1_000_000
        self.assertTrue(isinstance(_pd.EndingBalance, DataItem))
        self.assertTrue(_pd.EndingBalance.header, "Ending Balance")
        self.assertTrue(str(_pd.EndingBalance), "$1,000,000")

        # Success
        _pd.Success = False
        self.assertFalse(isinstance(_pd.Success, DataItem))
        self.assertTrue(_pd.EndingBalance.header, "Successful Period")
        self.assertTrue(str(_pd.EndingBalance), "False")

        # BankruptYear
        _pd.BankruptYear.data = 2005
        self.assertTrue(isinstance(_pd.BankruptYear, DataItem))
        self.assertTrue(_pd.BankruptYear.header, "Bankrupt Year")
        self.assertTrue(str(_pd.EndingBalance), "2005")

        _pd.BankruptYear = None
        self.assertTrue(str(_pd.EndingBalance), "-")

    def test_AllocationPeriod(self):
        _ap = AllocationPeriod(2000, 2020, 80, 15, 5)

        self.assertEqual(_ap.BeginYear, 2000)
        self.assertEqual(_ap.EndYear, 2020)
        self.assertEqual(_ap.pctStocks, 0.8)
        self.assertEqual(_ap.pctBonds, 0.15)
        self.assertEqual(_ap.pctCash, 0.05)

        _ap = AllocationPeriod(None, 2010, 75, 10, 15)

        self.assertEqual(_ap.BeginYear, 0)
        self.assertEqual(_ap.EndYear, 2010)
        self.assertEqual(_ap.pctStocks, 0.75)
        self.assertEqual(_ap.pctBonds, 0.10)
        self.assertEqual(_ap.pctCash, 0.15)

        _ap = AllocationPeriod(1990, None, 75, 10, 15)

        self.assertEqual(_ap.BeginYear, 1990)
        self.assertEqual(_ap.EndYear, 9999)
        self.assertEqual(_ap.pctStocks, 0.75)
        self.assertEqual(_ap.pctBonds, 0.10)
        self.assertEqual(_ap.pctCash, 0.15)

    def test_AnnualReturnData(self):
        # the returns of assets (stocks, bonds, cash) for a given year
        _ard = AnnualReturnData(2005, 8.8, 4.0, 0, 3.2)

        self.assertEqual(_ard.Year, 2005)
        self.assertAlmostEqual(_ard.Stocks, 0.088)
        self.assertAlmostEqual(_ard.Bonds, 0.04)
        self.assertAlmostEqual(_ard.Cash, 0.0)
        self.assertAlmostEqual(_ard.Inflation, 0.032)

    def test_HistoricalData(self):
        _hd = HistoricalData()
        _data = _hd.get_data(1928, 2025)

        self.assertEqual(len(_data), 98)

        # 1928 data
        self.assertEqual(_data[0].Year, 1928)
        self.assertTrue(isinstance(_data[0], AnnualReturnData))
        self.assertAlmostEqual(_data[0].Stocks, 0.4381)
        self.assertAlmostEqual(_data[0].Bonds, 0.0084)
        self.assertAlmostEqual(_data[0].Cash, 0.0)
        self.assertAlmostEqual(_data[0].Inflation, -0.0116)

        # 2025 data
        self.assertEqual(_data[-1].Year, 2025)
        self.assertTrue(isinstance(_data[-1], AnnualReturnData))
        self.assertAlmostEqual(_data[-1].Stocks, 0.1772)
        self.assertAlmostEqual(_data[-1].Bonds, 0.078)
        self.assertAlmostEqual(_data[-1].Cash, 0.0)
        self.assertAlmostEqual(_data[-1].Inflation, 0.0274)


if __name__ == "__main__":
    unittest.main()
