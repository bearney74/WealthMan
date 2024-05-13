from dataclass import dataclass

@dataclass
class Account:
    name:str
    balance: float = 0
    return_rate: float = 0.0
      
  def deposit(self, amount:float):
      self._balance+=amount
      
  def withdraw(self, amount:float):
      self._balance-=amount

  def calc_balance(self):
      self.balance*=(1.0+self.return_rate)

class TaxableAccount(Account):       #regular brokerage, bank savings acct.
  def __init__(self, name, balance, interest_rate):
      Account.__init__(self, name, balance, interest_rate)

class TaxDeferredAccount(Account):   #ie, pretax accounts..
  def __init__(self, name, balance, interest_rate):
      Account.__init__(self, name, balance, interest_rate)
      
class TaxFreeAccount(Account):    # ie, after tax, roth, etc
  def __init__(self, name, balance, interest_rate):
      Account.__init__(self, name, balance, interest_rate)