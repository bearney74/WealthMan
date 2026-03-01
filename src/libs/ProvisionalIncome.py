from .EnumTypes import FederalTaxStatusType
import logging

logger = logging.getLogger(__name__)


class SocialSecurityTaxes:
    def __init__(self, AGI: int, SS_Amount: int, filing_status: FederalTaxStatusType):
        self._SS_income = SS_Amount
        self._income = AGI + int(SS_Amount / 2)
        self._taxable = None

        if filing_status == FederalTaxStatusType.MARRIED_FILING_JOINTLY:
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
