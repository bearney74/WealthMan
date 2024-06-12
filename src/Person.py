from datetime import date
#from Account import Account

import datetime
from BasicInfo import BasicInfoTab

class Person:
  def __init__(self, Name, BirthDate, RetirementDate, LifeExpectancy, Relationship):
      self.Name=Name
      self.BirthDate=BirthDate              #date of birth
      self.RetirementDate=RetirementDate    
      self.LifeExpectancy=LifeExpectancy    #date of death (Dec 31st of year)
      self.Relationship=Relationship
      
  def set_LifeExpectancy_by_age(self, age: int):   #DOD = Date of Death
      assert isinstance(self.BirthDate, date)
      self.LifeExpectancy=date(self.BirthDate+age, 12, 31)    #set to Dec 31st of year
      
  def calc_age_by_date(self, dt: date) -> int:
      """ returns the number of years between two dates """
      return dt.year - self.BirthDate.year - ((dt.month, dt.day) < (self.BirthDate.month, self.BirthDate.day))
    
  def calc_age_by_year(self, year:int) -> int:   #get age of person on Dec 31st of year
      """ returns the age of person on Dec 31st of year """
      return self.calc_age_by_date(dt=date(year, 12, 31))
    
  def gui_import_data(self, b:BasicInfoTab, num):
      # num == "1" Client
      # num == "2" Spouse
      assert isinstance(b, BasicInfoTab)
      _year=datetime.datetime.now().year      
      b.import_data(num, self.Name,
                    str(abs(_year - self.BirthDate.year)),
                    str(self.RetirementDate.year - self.BirthDate.year),
                    str(self.LifeExpectancy.year - self.BirthDate.year),
                    self.Relationship)