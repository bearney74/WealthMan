from datetime import date

from .EnumTypes import IncomeType, AmountPeriodType, AccountOwnerType
from .IncomeExpenseBase import IncomeExpenseBase


class IncomeSource(IncomeExpenseBase):
    def __init__(
        self,
        Name: str,
        IncomeSource: IncomeType,
        Amount: int,
        AmountPeriod: AmountPeriodType,
        Owner: int,
        BeginDate: date = None,
        EndDate: date = None,
        SurvivorPercent: float = None,
        Taxable: bool = None,
        COLA: float = 0,
    ):
        IncomeExpenseBase.__init__(
            self, Name, Amount, AmountPeriod, BeginDate, EndDate, COLA=COLA
        )
        assert isinstance(IncomeSource, IncomeType)
        self.IncomeSource = IncomeSource
        
        assert isinstance (Owner, AccountOwnerType) or Owner is None
        self.Owner = Owner
        
        self.SurvivorPercent = SurvivorPercent
        self.Taxable = Taxable

"""
class SocialSecurity(IncomeSource):
    def __init__(
        self,
        Name: str,
        FRA: int,
        FRAAmount: int,
        Amount: int,
        Owner: int,
        BeginDate: date = None,
        COLA: float = 0,
    ):
        IncomeSource.__init__(
            self,
            Name,
            IncomeType.SocialSecurity,
            Amount,
            AmountPeriodType.Annual,
            Owner,
            BeginDate,
            COLA=COLA,
        )

        self.FRA = FRA
        self.FRAAmount = FRAAmount

    #  def _calc_balance(self) -> int:
    #      if self._annual_income == 0:
    #         self._annual_income=self._calc_annual_income()

    # print("Social Security")
    #      self._annual_income = int(self._annual_income * (1.0 + self.COLA/100.0))    #fix me!!
    #      return self._annual_income

    def calc_Full_Retirement_Age(self, date_of_birth: date) -> date:
        if date_of_birth.year > 1960:
            return date(date_of_birth.year + 67, date_of_birth.month, date_of_birth.day)
        else:
            assert False
            # todo
"""