from datetime import date

from .IncomeExpenseBase import IncomeExpenseBase
from .EnumTypes import AmountPeriodType


class Expense(IncomeExpenseBase):
    def __init__(
        self,
        Name: str,
        Amount: int,
        AmountPeriod: AmountPeriodType,
        BeginDate: date = None,
        EndDate: date = None,
        COLA: float = 0.0,
    ):
        IncomeExpenseBase.__init__(
            self, Name, Amount, AmountPeriod, BeginDate, EndDate, COLA=COLA
        )
