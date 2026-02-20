from .EnumTypes import FederalTaxStatusType
import logging

logger = logging.getLogger(__name__)

class SocialSecurityTaxes:
    def __init__(self, AGI: int, SS_Amount: int, filing_status:FederalTaxStatusType):
        self._SS_income = SS_Amount
        self._income = AGI + int(SS_Amount / 2)
        self._taxable = None

        if filing_status == FederalTaxStatusType.MarriedFilingJointly:
           self._threshold1 = 32000
           self._threshold2 = 44000
        else:
           self._threshold1 = 25000
           self._threshold2 = 34000
            

    def do_calcs(self):
        self._taxable = 0

        if self._income < self._threshold1:
            return  # none of the SS income is taxable

        # over $32000 income is taxable at 0.5
        self._taxable = (self._income - self._threshold1) * 0.5

        if self._income > self._threshold2:
            self._taxable += (self._income - self._threshold2) * 0.35

        # we know want to take the lesser of 85% of income, or the current value of taxable
        self._taxable = min(self._SS_income * 0.85, self._taxable)

        # round down to nearest dollar
        self._taxable = int(self._taxable)

    def taxable(self):
        if self._taxable is None:
            self.do_calcs()

        return self._taxable

    def percent_taxable(self):
        return round(100.0 * (self.taxable() / self._SS_income), 2)


if __name__ == "__main__":
    # examples taken from https://www.youtube.com/watch?v=-ifv6Y6migk&list=PL63mgCrh_1ym4wKoUgFbNazFwmOHVjl6V
    sst = SocialSecurityTaxes(0, 48000, FederalTaxStatusType.MarriedFilingJointly)
    assert sst.taxable() == 0
    assert sst.percent_taxable() == 0

    sst = SocialSecurityTaxes(13200, 48000, FederalTaxStatusType.MarriedFilingJointly)
    assert sst.taxable() == 2600
    assert sst.percent_taxable() == 5.42

    sst = SocialSecurityTaxes(70000, 48000, FederalTaxStatusType.MarriedFilingJointly)
    assert sst.taxable() == 40800
    assert sst.percent_taxable() == 85.0
