from dataclass import dataclass
from datetime import date
from Account import Account

@dataclass
class Person:
    name:str
    DOB:datetime.date = None         #date of birth
    DOD:datetime.date = None         #date of death (Dec 31st of year)
    accounts: list(Account)

  def add_account(self, account:Account):
      self._accounts.append(account)
      
  def remove_account(self, account:Account):
      self._accounts.remove(account)
      
  def set_DOD_by_age(self, age: int):
      assert isinstance(self.DOB, date)
      self.DOD=date(self.DOB+age, 12, 31)    #set to Dec 31st of year