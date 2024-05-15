from dataclasses import dataclass
from datetime import date
from EnumTypes import IncomeType, AmountPeriodType

@dataclass
class IncomeSource:
    Name:str
    IncomeSource: IncomeType
    Amount:int
    AmountPeriod: AmountPeriodType   #Annual, Monthly, bi-weekly, weekly
    BeginDate: date
    #EndDate: date
    Owner: int
    SurvivorPercent: float = None
    Taxable: bool = None
    COLA: float = None
    EndDate: date = None
    FRA: int = None
    FRAAmount: float = None
    
    _annual_income: int = 0
    def calc_income_by_year(self, year) -> int:
        #if this income begin year is still in the future..  (no need to check the end date)
        if self.BeginDate is not None and self.BeginDate.year > year:
           return 0
        
        #no Begin Date and no end date or the enddate is still in the future
        if self.BeginDate is None:
           if self.EndDate is None or self.EndDate.year > year:
              return self._calc_income()
       
        return 0
        
    def _calc_annual_income(self) -> int:
         if self.AmountPeriod == AmountPeriodType.Annual:
            return self.Amount
         if self.AmountPeriod == AmountPeriodType.Monthly:
            return self.Amount * 12
         if self.AmountPeriod == AmountPeriodType.BiWeekly:
            return self.Amount * 26
         if self.AmountPeriod == AmountPeriodType.Weekly:
            return self.Amount * 52
        
         print("We shouldn't get here: IncomeSources.py, calc_income_by_year function, AmountPeriod='%s'" % self.AmountPeriod)
      
         #dont know what to do.. just return Amount
         return self.Amount
      
    def _calc_income(self) -> int:
        if self._annual_income == 0:
            self._annual_income=self._calc_annual_income()
            #return self._annual_income()
        
        if self.COLA != 0 and self.COLA is not None:
           self._annual_income=int(self._annual_income * (1.0 + self.COLA/100.0))
           return self._annual_income
        
        return self._annual_income