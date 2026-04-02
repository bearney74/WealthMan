import unittest

from src.libs.FederalTax import FederalTax
from src.libs.EnumTypes import FederalTaxStatusType

# should we continue to update these tests each year, or should we look for a way just to test
# some standard xml data input, and use that instead?


class FederalTaxTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_single_standard_tax_deduction(self):
        _ft = FederalTax(FileStatus=FederalTaxStatusType.SINGLE)
        self.assertEqual(16100, _ft.StandardDeduction)

    def test_marriedjointly_standard_tax_deduction(self):
        _ft = FederalTax(FileStatus=FederalTaxStatusType.MARRIED_FILING_JOINTLY)
        self.assertEqual(32200, _ft.StandardDeduction)

    def test_marriedseparate_standard_tax_deduction(self):
        _ft = FederalTax(FileStatus=FederalTaxStatusType.MARRIED_FILING_SEPARATELY)
        self.assertEqual(16100, _ft.StandardDeduction)

    def test_HeadOfHousehold_standard_tax_deduction(self):
        _ft = FederalTax(FileStatus=FederalTaxStatusType.HEAD_OF_HOUSEHOLD)
        self.assertEqual(24150, _ft.StandardDeduction)

    def test_single_calcs(self):
        _tax = FederalTax(FileStatus=FederalTaxStatusType.SINGLE)

        for _amount, _taxes in (
            (100, 10),
            (20000, 2152),
            (60000, 7912),  # 12400 x 0.10,  38000 x 0.12,   9600 x 0.22
        ):
            self.assertEqual(
                _tax.calc_taxes(_amount),
                _taxes,
                "Taxable Income=$%s, expected taxes=$%s" % (_amount, _taxes),
            )

    def test_marriedjointly_calcs(self):
        _tax = FederalTax(FileStatus=FederalTaxStatusType.MARRIED_FILING_JOINTLY)

        for _amount, _taxes in (
            (100, 10),  # 100 x 0.10
            (20000, 2000),  # 20000 x 0.10
            (60000, 6704),  # 24800 x 0.10 , 35200 * 0.12
            (150000, 22424),  # 24800 x 0.10 , 76000 * 0.12, 49200 * 0.22
        ):
            self.assertEqual(
                _tax.calc_taxes(_amount),
                _taxes,
                "Taxable Income=$%s, expected taxes=$%s" % (_amount, _taxes),
            )

    def effective_tax_rate(self):
        _tax = FederalTax(FileStatus=FederalTaxStatusType.MARRIED_FILING_JOINTLY)

        self.assertEqual(0.0, _tax.effective_tax_rate(taxes=0, total_income=0))
        self.assertEqual(
            25.0, _tax.effective_tax_rate(taxes=25_000, total_income=100_000)
        )

    def test_marginal_tax_rate(self):
        _tax = FederalTax(FileStatus=FederalTaxStatusType.MARRIED_FILING_JOINTLY)
        self.assertEqual(_tax.marginal_tax_rate(10_000), 0.0)

        self.assertEqual(_tax.marginal_tax_rate(40_000), 10.0)


if __name__ == "__main__":
    unittest.main()
