from datetime import date

from .IncomeExpenseBase import IncomeExpenseBase
from .EnumTypes import AmountPeriodType


class Expense(IncomeExpenseBase):
    def __init__(
        self,
        Name: str,
        Amount: int,
        AmountPeriod: AmountPeriodType,
        BirthDate: date=None,
        BeginAge: int = None,
        EndAge: int = None,
        COLA: float = 0.0,
    ):
        IncomeExpenseBase.__init__(
            self, Name=Name, Amount=Amount, AmountPeriod=AmountPeriod,
            BirthDate=BirthDate, BeginAge=BeginAge, EndAge=EndAge, COLA=COLA
        )
