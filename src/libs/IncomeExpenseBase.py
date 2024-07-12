from datetime import date

from .EnumTypes import AmountPeriodType
from .DateHelper import DateHelper

import logging

logger = logging.getLogger(__name__)


class IncomeExpenseBase:
    def __init__(
        self,
        Name: str,
        Amount: int,
        AmountPeriod: AmountPeriodType,
        BirthDate: date = None,
        BeginAge: int = None,
        EndAge: int = None,
        LifeSpanAge: int = None,
        SurvivorPercent: float = 0.0,
        COLA: float = 0.0,
    ):
        self.BirthDate = BirthDate

        assert isinstance(Name, str)
        self.Name = Name

        assert isinstance(Amount, int)
        self.Amount = Amount

        assert isinstance(AmountPeriod, AmountPeriodType)
        self.AmountPeriod = AmountPeriod

        if BeginAge is None:
            BeginAge = 0
        if EndAge is None:
            EndAge = 99

        if LifeSpanAge is None:
            LifeSpanAge = 99

        self.BeginDate = date(BirthDate.year + BeginAge, BirthDate.month, BirthDate.day)
        self.LifeSpanDate = date(
            BirthDate.year + LifeSpanAge, BirthDate.month, BirthDate.day
        )
        self.EndDate = date(BirthDate.year + EndAge, BirthDate.month, BirthDate.day)

        self.SurvivorPercent = SurvivorPercent
        assert isinstance(COLA, float) or COLA is None
        if COLA is None:
            COLA = 0.0
        self.COLA = COLA

        self._annual_balance = 0

    def calc_balance_by_year(self, year) -> int:
        # this income source is still in the future..  just return 0.
        if self.BeginDate.year > year:
            return 0

        # this income source is in the past..  just return 0
        if self.EndDate.year < year:
            return 0

        # check for a full year of income  #this is the usual case...
        if self.BeginDate.year < year and self.EndDate.year > year:
            return self._calc_balance()

        if self.BeginDate.year == year:
            if self.EndDate.year > year:
                _dh = DateHelper(self.BeginDate, date(year, 12, 31))
                return int(_dh.percent_of_year() / 100.0 * self._calc_balance())
            else:  # Endyear also equal to year
                _dh = DateHelper(self.BeginDate, self.EndDate)
                return int(_dh.percent_of_year() / 100.0 * self._calc_balance())
                # return self._annual_income
        if self.EndDate.year == year:
            if self.BeginDate.year < year:
                _dh = DateHelper(date(year, 1, 1), self.EndDate)
                return int(_dh.percent_of_year() / 100.0 * self._calc_balance())
            else:  # begin date is also equal to year
                _dh = DateHelper(self.BeginDate, self.EndDate)
                return int(_dh.percent_of_year() / 100.0 * self._calc_balance())

        # we shouldn't get here..
        logger.error("Something went wrong calculating balance for income/expense")
        logger.error(
            "year=%s, Begin Year=%s, End Year=%s"
            % (year, self.BeginDate.year, self.EndDate.year)
        )
        assert False

    def _calc_annual_balance(self) -> int:
        assert self.AmountPeriod == AmountPeriodType.Annual
        return self.Amount

    def _calc_balance(self) -> int:
        if self._annual_balance == 0:
            self._annual_balance = self._calc_annual_balance()
            return self._annual_balance

        if self.COLA != 0:
            self._annual_balance = int(self._annual_balance * (1.0 + self.COLA / 100.0))
            return self._annual_balance

        return self._annual_balance
