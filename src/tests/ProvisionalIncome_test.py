import unittest

from libs.ProvisionalIncome import ProvisionalIncome
from libs.EnumTypes import FederalTaxStatusType


class ProvisionalIncomeTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_single_status(self):
        _p = ProvisionalIncome(FederalTaxStatusType.Single)
        self.assertEqual(_p.get_rate(10_000, 15_000), 0.0)
        self.assertEqual(_p.calc_ss_taxable(10_000, 15_000), 0)

        self.assertEqual(_p.get_rate(20_000, 15_000), 50.0)
        self.assertEqual(_p.calc_ss_taxable(20_000, 15_000), int(0.50 * 15_000))

        self.assertEqual(_p.get_rate(30_000, 15_000), 85.0)
        self.assertEqual(_p.calc_ss_taxable(30_000, 15_000), int(0.85 * 15_000))

    def test_married_status(self):
        _p = ProvisionalIncome(FederalTaxStatusType.MarriedFilingJointly)
        self.assertEqual(_p.get_rate(20_000, 15_000), 0.0)
        self.assertEqual(_p.calc_ss_taxable(20_000, 15_000), 0)

        self.assertEqual(_p.get_rate(30_000, 15_000), 50.0)
        self.assertEqual(_p.calc_ss_taxable(30_000, 16_000), int(0.50 * 16_000))

        self.assertEqual(_p.get_rate(40_000, 15_000), 85.0)
        self.assertEqual(_p.calc_ss_taxable(40_000, 17_000), int(0.85 * 17_000))


if __name__ == "__main__":
    unittest.main()
