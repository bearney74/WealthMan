import IncomeExpenseBase
from EnumTypes import IncomeType, AmountPeriodType
from datetime import date

class Expense(IncomeExpenseBase.IncomeExpenseBase):
  def __init__(self, Name:str, Amount:int, AmountPeriod:AmountPeriodType,
               BeginDate:date=None, EndDate:date=None, COLA: float=0.0):
      IncomeExpenseBase.IncomeExpenseBase.__init__(self, Name, Amount, AmountPeriod, BeginDate, EndDate, COLA=COLA)
      #self.Name=Name
      #self.Amount=Amount
      #self.AmountPeriod=AmountPeriod
      #self.BeginDate=BeginDate
      #self.EndDate=EndDate
      #self.COLA=COLA
   
      #self._expense_balance=0