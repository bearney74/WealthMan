from datetime import date

from .IncomeExpenseBase import IncomeExpenseBase


class Expense(IncomeExpenseBase):
    def __init__(
        self,
        Name: str,
        Amount: int,
        BirthDate: date = None,
        BeginAge: int = None,
        EndAge: int = None,
        COLA: float = 0.0,
    ):
        IncomeExpenseBase.__init__(
            self,
            Name=Name,
            Amount=Amount,
            BirthDate=BirthDate,
            BeginAge=BeginAge,
            EndAge=EndAge,
            COLA=COLA,
        )
