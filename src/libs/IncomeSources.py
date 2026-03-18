from datetime import date

from .EnumTypes import (
    IncomeSourceType,
    PersonType,
)

from .Person import Person
from .MiscLibs import PeriodValidator

import logging

logger = logging.getLogger(__name__)


class IncomeSource:
    def __init__(
        self,
        Name: str,
        IncomeType: IncomeSourceType,
        Amount: int,
        Owner: PersonType,
        Period: PeriodValidator,
        COLA: float = 0.0,
    ):
        assert isinstance(Period, PeriodValidator)
        self._period = Period

        assert isinstance(Name, str)
        self.Name = Name

        assert isinstance(Amount, int)
        self.Amount = Amount

        assert isinstance(COLA, float) or COLA is None
        if COLA is None:
            COLA = 0.0
        self.COLA = COLA

        self._COLA_Flag = COLA != 0.0

        self._initial_income = Amount
        # annual variables
        # self._balance = 0
        self._ss_income = 0
        self._taxable_income = 0
        self._income = 0

    def set_COLA_Flag(self, flag: bool):
        self._COLA_Flag = flag

    def get_COLA_Flag(self):
        return self._COLA_Flag

    @property
    def ss_income(self):
        return self._ss_income

    @property
    def taxable_income(self):
        return self._taxable_income

    def calc_income_by_year(self, year, inflation=0.0) -> int:
        # this income source is still in the future..  just return 0.
        self._ss_income = 0
        self._taxable_income = 0

        if self._period.isa_valid_period(year):
            return self._calc_income(inflation)

        return 0

    def _calc_income(self, inflation=0.0) -> int:
        if self._income == 0:
            self._income = self._initial_income
            self._taxable_income = self._income
            return self._income

        self._income = int(self._income * (1.0 + (self.COLA - inflation) / 100.0))

        self._taxable_income = self._income
        return self._income


class SocialSecurity(IncomeSource):
    def __init__(
        self,
        Name: str,
        Person: Person,
        FRAAmount: int,
        Owner: PersonType,
        BirthDate: date,
        BeginAge: int,
        COLA: float = 0.0,
    ):
        # table used to figure out the SS benefit based on Age benefits start...
        self._table: dict[int, float] = {
            62: 0.7,
            63: 0.75,
            64: 0.80,
            65: 0.866667,
            66: 0.933333,
            67: 1.0,
            68: 1.08,
            69: 1.16,
            70: 1.24,
        }

        self.FRAAmount = FRAAmount

        # need to calculate Amount from FRAAmount and birthdate...
        # assert BeginAge in self._table.keys()
        # Amount = int(self.FRAAmount * self._table[BeginAge])

        self.SpouseObj: Person = None
        self.Person: Person = Person

        assert BeginAge >= 62

        _amount = self.calc_benefit_amount_by_age(BeginAge)
        _period = PeriodValidator(birthYear=BirthDate.year, beginAge=BeginAge)
        super(SocialSecurity, self).__init__(
            Name=Name,
            IncomeType=IncomeSourceType.SOCIAL_SECURITY,
            Amount=_amount,
            Owner=Owner,
            Period=_period,
            COLA=COLA,
        )

        self.set_COLA_Flag(True)  ## SS always has a COLA

    @property
    def ss_income(self):
        return self._income

    def set_SpouseSS(self, SpouseObj):
        # this is used for survivor benefits (ie max(clientBenefit, spouse Benefit)
        self.SpouseObj = SpouseObj

    def calc_income_by_year(self, year, inflation=0.0) -> int:
        super().calc_income_by_year(year, inflation)
        self._ss_income = self._income
        self._taxable_income = (
            0  # don't calc this here.. need to know all income to calc this value
        )

        return self._income

    def calc_full_retirement_age(self):
        if self.Person.birthDate.year >= 1960:
            return 67
        return 66

    def calc_benefit_amount_by_age(self, age: int):
        assert isinstance(age, int)

        if self.calc_full_retirement_age() == 67:
            if age in self._table:
                _ratio = self._table[age]
                return round(self.FRAAmount * _ratio)
            if age < 62:
                return 0
            if age > 70:
                return round(self.FRAAmount * self._table[70])

        # fix me!
        return self.FRAAmount
        raise AssertionError
