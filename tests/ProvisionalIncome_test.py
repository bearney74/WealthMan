import unittest

from src.libs.ProvisionalIncome import SocialSecurityTaxes
from src.libs.EnumTypes import FederalTaxStatusType


class ProvisionalIncomeTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_single_status(self):
        sst = SocialSecurityTaxes(0, 48000, FederalTaxStatusType.SINGLE)
        assert sst.taxable() == 0
        assert sst.percent_taxable() == 0

    def test_married_status(self):
        # examples taken from https://www.youtube.com/watch?v=-ifv6Y6migk&list=PL63mgCrh_1ym4wKoUgFbNazFwmOHVjl6V
        sst = SocialSecurityTaxes(0, 48000, FederalTaxStatusType.MARRIED_FILING_JOINTLY)
        assert sst.taxable() == 0
        assert sst.percent_taxable() == 0

        sst = SocialSecurityTaxes(
            13200, 48000, FederalTaxStatusType.MARRIED_FILING_JOINTLY
        )
        assert sst.taxable() == 2600
        assert sst.percent_taxable() == 5.42

        sst = SocialSecurityTaxes(
            70000, 48000, FederalTaxStatusType.MARRIED_FILING_JOINTLY
        )
        assert sst.taxable() == 40800
        assert sst.percent_taxable() == 85.0


if __name__ == "__main__":
    unittest.main()
