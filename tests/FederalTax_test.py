import unittest

from src.libs.FederalTax import FederalTax
from src.libs.EnumTypes import FederalTaxStatusType

Year = 2024


class FederalTaxTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_single_standard_tax_deduction(self):
        _ft = FederalTax(FileStatus=FederalTaxStatusType.SINGLE, Year=Year)
        self.assertEqual(14600, _ft.StandardDeduction)

    def test_marriedjointly_standard_tax_deduction(self):
        _ft = FederalTax(
            FileStatus=FederalTaxStatusType.MARRIED_FILING_JOINTLY, Year=Year
        )
        self.assertEqual(29200, _ft.StandardDeduction)

    def test_marriedseparate_standard_tax_deduction(self):
        _ft = FederalTax(
            FileStatus=FederalTaxStatusType.MARRIED_FILING_SEPARATELY, Year=Year
        )
        self.assertEqual(14600, _ft.StandardDeduction)

    def test_HeadOfHousehold_standard_tax_deduction(self):
        _ft = FederalTax(FileStatus=FederalTaxStatusType.HEAD_OF_HOUSEHOLD, Year=Year)
        self.assertEqual(21900, _ft.StandardDeduction)

    def test_single_calcs(self):
        _tax = FederalTax(FileStatus=FederalTaxStatusType.SINGLE, Year=Year)

        for _amount, _taxes in (
            (100, 10),
            (20000, 2167),
            (47150, 5425),
        ):
            self.assertEqual(
                _tax.calc_taxes(_amount),
                _taxes,
                "Taxable Income=$%s, expected taxes=$%s" % (_amount, _taxes),
            )

    def test_marriedjointly_calcs(self):
        _tax = FederalTax(
            FileStatus=FederalTaxStatusType.MARRIED_FILING_JOINTLY, Year=Year
        )

        for _amount, _taxes in (
            (100, 10),
            (20000, 2000),
            (47150, 5193),
            (150000, 23105),
        ):
            self.assertEqual(
                _tax.calc_taxes(_amount),
                _taxes,
                "Taxable Income=$%s, expected taxes=$%s" % (_amount, _taxes),
            )


if __name__ == "__main__":
    unittest.main()
