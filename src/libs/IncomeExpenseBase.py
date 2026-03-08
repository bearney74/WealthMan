from datetime import date

import logging

logger = logging.getLogger(__name__)


class IncomeExpenseBase:
    def __init__(
        self,
        Name: str,
        Amount: int,
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

        if SurvivorPercent is None:
            SurvivorPercent = 0.0
        self.SurvivorPercent = SurvivorPercent

        assert isinstance(COLA, float) or COLA is None
        if COLA is None:
            COLA = 0.0
        self.COLA = COLA

        self._COLA_Flag = COLA != 0.0

        self._annual_balance = 0

    def set_COLA_Flag(self, flag: bool):
        self._COLA_Flag = flag

    def get_COLA_Flag(self):
        return self._COLA_Flag

    def calc_balance_by_year(self, year, inflation=0.0) -> int:
        # this income source is still in the future..  just return 0.
        if self.BeginDate.year > year:
            return 0

        # this income source is in the past..  just return 0
        if self.EndDate.year < year:
            return 0

        # check for a full year of income  #this is the usual case...
        # we assume each year goes in order (2004-> 2005, -> 2006)
        # if self.BeginDate.year < year and self.EndDate.year > year:
        return self._calc_balance(inflation)

    def _calc_annual_balance(self) -> int:
        return self.Amount

    def _calc_balance(self, inflation=0.0) -> int:
        if self._annual_balance == 0:
            self._annual_balance = self._calc_annual_balance()
            return self._annual_balance

        self._annual_balance = int(
            self._annual_balance * (1.0 + (self.COLA - inflation) / 100.0)
        )
        return self._annual_balance
