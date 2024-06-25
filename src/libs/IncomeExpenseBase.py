from datetime import date

from .EnumTypes import AmountPeriodType
from .DateHelper import DateHelper


class IncomeExpenseBase:
    def __init__(
        self,
        Name: str,
        Amount: int,
        AmountPeriod: AmountPeriodType,
        BeginDate: int = None,
        EndDate: int = None,
        #SurvivorPercent: float = None,
        #Taxable: bool = None,
        COLA: float = 0.0,
    ):
        assert isinstance(Name, str)
        self.Name = Name
        # self.IncomeSource=IncomeType

        assert isinstance(Amount, int)
        self.Amount = Amount

        assert isinstance(AmountPeriod, AmountPeriodType)
        self.AmountPeriod = AmountPeriod

        assert isinstance(BeginDate, date) or BeginDate is None
        self.BeginDate = BeginDate
        # self.Owner=Owner
        #self.SurvivorPercent = SurvivorPercent
        #self.Taxable = Taxable
        assert isinstance(COLA, float) or COLA is None
        if COLA is None:
            COLA = 0.0
        self.COLA = COLA
        
        assert isinstance(EndDate, date) or EndDate is None
        self.EndDate = EndDate

        self._annual_balance = 0

    def calc_balance_by_year(self, year) -> int:
        # this income source has no begin or end date..  so it should be calculated..
        if self.BeginDate is None and self.EndDate is None:
            return self._calc_balance()

        if self.BeginDate is None:  # end date is not None
            assert self.EndDate is not None

            if self.EndDate.year < year:
                return 0
            if self.EndDate.year > year:
                return self._calc_balance()

            assert self.EndDate.year == year

            _dh = DateHelper(self.BeginDate, self.EndDate)
            self._annual_balance = int(
                _dh.percent_of_year() / 100.0 * self._calc_balance()
            )
            return self._annual_balance

        elif self.EndDate is None:  # begin date is not None
            assert self.BeginDate is not None

            if self.BeginDate.year > year:  # income source has not started yet.
                return 0
            if self.BeginDate.year < year:  # this income source has started..
                # this is a full year's worth of income
                return self._calc_balance()

            assert self.BeginDate.year == year

            _dh = DateHelper(self.BeginDate, date(self.BeginDate.year, 12, 31))
            self._annual_income = int(
                _dh.percent_of_year() / 100.0 * self._calc_balance()
            )
            return self._annual_balance

        # if we get here both BeginDate and EndDate should not be None
        assert self.BeginDate is not None
        assert self.EndDate is not None

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
                self._annual_income = int(
                    _dh.percent_of_year() / 100.0 * self._calc_balance()
                )
                return self._annual_income
        elif self.EndDate.year == year:
            if self.BeginDate.year < year:
                _dh = DateHelper(date(year, 1, 1), self.EndDate)
                return int(_dh.percent_of_year() / 100.0 * self._calc_balance())
            else:  # begin date is also equal to year
                _dh = DateHelper(self.BeginDate, self.EndDate)
                return int(_dh.percent_of_year() / 100.0 * self._calc_balance())

        # we shouldn't get here..
        # print(year, self.BeginDate, self.EndDate)
        assert False

    def _calc_annual_balance(self) -> int:
        assert self.AmountPeriod == AmountPeriodType.Annual
        return self.Amount
        
    def _calc_balance(self) -> int:
        if self._annual_balance == 0:
            self._annual_balance = self._calc_annual_balance()
            return self._annual_balance

        if self.COLA != 0 and self.COLA is not None:
            self._annual_balance = int(self._annual_balance * (1.0 + self.COLA / 100.0))
            return self._annual_balance

        return self._annual_balance
