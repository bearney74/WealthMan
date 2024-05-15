from dataclasses import dataclass
from datetime import date
#from Account import Account

@dataclass
class Person:
  Name:str
  BirthDate:date              #date of birth
  RetirementDate:date=None    
  LifeExpectancy:date=None    #date of death (Dec 31st of year)
  Relationship:str=None
      
  def set_LifeExpectancy_by_age(self, age: int):   #DOD = Date of Death
      assert isinstance(self.BirthDate, date)
      self.LifeExpectancy=date(self.BirthDate+age, 12, 31)    #set to Dec 31st of year
      
  def calc_age_by_date(self, dt: date) -> int:
      """ returns the number of years between two dates """
      return dt.year - self.BirthDate.year - ((dt.month, dt.day) < (self.BirthDate.month, self.BirthDate.day))
    
  def calc_age_by_year(self, year:int) -> int:   #get age of person on Dec 31st of year
      """ returns the age of person on Dec 31st of year """
      return self.calc_age_by_date(dt=date(year, 12, 31))