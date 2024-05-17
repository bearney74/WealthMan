from dataclasses import dataclass
from datetime import date
from EnumTypes import IncomeType, AmountPeriodType
from DateHelper import DateHelper


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
        #this income source has no begin or end date..  so it should be calculated..
        if self.BeginDate is None and self.EndDate is None:
           return self._calc_income()
        
        if self.BeginDate is None:    #end date is not None
           assert(self.EndDate is not None)
        
           if self.EndDate.year < year:
              return 0
           if self.EndDate.year > year:
              return self._calc_income()
           assert(self.EndDate.year == year)
        
           _dh=DateHelper(self.BeginDate, self.EndDate)
           self._annual_income=int(_dh.percent_of_year()/100.0 * self._calc_income())
           return self._annual_income
        
        elif self.EndDate is None:    #begin date is not None
           assert(self.BeginDate is not None)
           
           if self.BeginDate.year > year:  # income source has not started yet.
               return 0
           if self.BeginDate.year < year:   #this income source has started..
               #this is a full year's worth of income
               return self._calc_income()
           assert(self.BeginDate.year == year)
           
           _dh=DateHelper(self.BeginDate, date(self.BeginDate.year, 12, 31))
           self._annual_income=int(_dh.percent_of_year()/100.0 * self._calc_income())
           return self._annual_income
            
        # if we get here both BeginDate and EndDate should not be None
        assert (self.BeginDate is not None)
        assert (self.EndDate is not None)
        
        # this income source is still in the future..  just return 0.
        if self.BeginDate.year > year:
           return 0
        
        #this income source is in the past..  just return 0
        if self.EndDate.year < year:
           return 0
        
        #check for a full year of income  #this is the usual case...
        if self.BeginDate.year < year and self.EndDate.year > year:
           return self._calc_income()
        #elif self.BeginDate.year < year and self.EndDate.year == year:
            
        #the income source begins and/or ends with this year..       
        #the rest of the cases deal with a partial year, where we start a new job (income source) midyear,
        #or we quite a job (income source) mid year.
            
        if self.BeginDate.year == year:
           if self.EndDate.year > year:
              _dh=DateHelper(self.BeginDate, date(year, 12, 31))
              #print(_dh.percent_of_year())
              #self._annual_income=
              return int(_dh.percent_of_year()/100.0 * self._calc_income())
              #return self._annual_income
           else:  #Endyear also equal to year
              _dh=DateHelper(self.BeginDate, self.EndDate)
              self._annual_income=int(_dh.percent_of_year()/100.0 * self._calc_income()) 
              return self._annual_income
        elif self.EndDate.year == year:
           if self.BeginDate.year < year:
              _dh=DateHelper(date(year, 1, 1), self.EndDate)
              #self._annual_income=
              return int(_dh.percent_of_year()/100.0 * self._calc_income()) 
              #return self._annual_income
           else: #begin eate is also equal to year
              _dh=DateHelper(self.BeginDate, self.EndDate)
              #self._annual_income=
              return int(_dh.percent_of_year()/100.0 * self._calc_income()) 
              #return self._annual_income
                             
                
        #we shouldn't get here..
        print(year, self.BeginDate, self.EndDate)
        assert(False)
        #if self.BeginDate.year == year and self.EndDate.year == year:
        #   _dh=DateHelper(self.BeginDate, self.EndDate)
        #   self._annual_income=int(_dh.percent_of_year * self._calc_income()) 
        #   return self._annual_income
        
        #if self.BeginDate.year == year:
        #   _end_of_year = datetime.date(year,12,31)
        #   _diff = _end_of_year - self.BeginDate
        #   self._annual_income=(self._calc_annual_income() * _diff/365.25) * (1.0 + self.COLA/100.0)
        #   return self._annual_income
        #elif self.EndDate.year == year:
        #   _beginning_of_year=datetime.date(year, 1, 1)
        #   _diff = self.EndDate - _beginning_of_year
        #   self._annual_income=(self._calc_annual_income() * _diff/365.25) * (1.0 + self.COLA/100.0)
        #   return self._annual_income
        
        #print(f"Name:{self.Name}, Begin Date:{self.BeginDate}, End Date:{self.EndDate}, Amount:{self.Amount}")
        #assert (False)    #will cause an error since we shouldn't get here and we do..
        
        #return 0
        
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
        
        #if "Pension" in self.Name:
        #    print(self.COLA, self.Amount, self._annual_income, self.AmountPeriod)
        
        if self.IncomeSource == IncomeType.SocialSecurity:
            print("Social Security")
            self._annual_income = int(self._annual_income * 1.03)    #fix me!!
            return self._annual_income
        
        if self.COLA != 0 and self.COLA is not None:
           self._annual_income=int(self._annual_income * (1.0 + self.COLA/100.0))
           return self._annual_income

        return self._annual_income
    
    
class SocialSecurity(IncomeSource):

  def set_COLA(self, COLA):
      if COLA is None:
          #produce an error, it should be 0 or something similar (1,2,3, etc)
          print("Error, Social Security COLA has not been set")
          self.COLA=0

      self.COLA = COLA

  def _calc_income(self) -> int:
      if self._annual_income == 0:
         self._annual_income=self._calc_annual_income()
        
      print("Social Security")
      self._annual_income = int(self._annual_income * (1.0 + self.COLA/100.0))    #fix me!!
      return self._annual_income

  def calc_Full_Retirement_Age(self, date_of_birth:date) -> date:
      if date_of_birth.year > 1960:
          return date(date_of_birth.year + 67, date_of_birth.month, date_of_birth.day)
      else:
          assert(False)
          #todo