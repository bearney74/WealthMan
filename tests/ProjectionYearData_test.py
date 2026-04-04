import unittest

from src.libs.Projections import ProjectionYearData


class ProjectionYearDataTest(unittest.TestCase):
    def test_DataItemHeaders(self):
        _p = ProjectionYearData(2000)

        self.assertEqual(_p.projectionYear.data, 2000)

        self.assertEqual(_p.taxableIncomeTotal.header, "Total Taxable Income")
        self.assertEqual(_p.incomeTotal.header, "Income Total")

        self.assertEqual(_p.FPL.header, "FPL")
        self.assertEqual(_p.ssIncomeTotal.header, "SS Income Total")
        self.assertEqual(_p.ssTaxableIncome.header, "SS Taxable Income")
        self.assertEqual(_p.ssTaxRate.header, "SS Tax Rate")
        self.assertEqual(_p.expenseTotal.header, "Expense Total")

        self.assertEqual(_p.netIncome.header, "Net Income")
        # self.assertEqual(_p.surplusDeficit.header, "Surplus Deficit")
        self.assertEqual(_p.thisYearsFederalTaxes.header, "This Years Federal Taxes")
        # self.assertEqual(self..header, "")


if __name__ == "__main__":
    unittest.main()
