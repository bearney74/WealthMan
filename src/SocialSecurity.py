from datetime import date

from Person import Person

class SocialSecurity:
  def __init__(self, benefit_amount:int, benefit_reduction:float, start_date:date, end_date:date=None, COLA:float=0.0, FRA:int=None,
               FRAAmount:int=0):
      self.benefit_amount=benefit_amount
      self.benefit_reduction=benefit_reduction
      self.start_date=start_date
      self.end_date=end_date
      
      self.COLA=COLA
      self.FRA=FRA
      self.FRAAmount=FRAAmount
    
  def calc_full_retirement_age(self, person:Person):
      if person.BirthDate > date(1960, 1, 1):
         return 67
      return 66
    
  def calc_end_date(self, person:Person):
      self.end_date = date(person.Birthdate.year + person.LifeExpectancy, person.BirthDate.month, person.BirthDate.day)
      