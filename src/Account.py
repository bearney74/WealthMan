from dataclass import dataclass

@dataclass
class Account:
    Name:str
    Type:AccountType
    Balance: float = 0
    COLA: float = 0.0
      
  def deposit(self, amount:float):
      self.Balance+=amount
      
  def withdraw(self, amount:float):
      self.Balance-=amount

  def calc_payment(self):
      return self.balance*self.COLA
    

@dataclass
class AllocationPeriod:
    Name:str
    BeginDate:date
    EndDate:date
    PercentStocks:float
    PercentBonds: float
    PercentMoneyMarket:float