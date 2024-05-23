from datetime import date
from EnumTypes import AccountType

class Account:
  def __init__(self, Name:str, Type: AccountType, Owner:str, Balance:int=0, COLA:float=0):
      
      assert(isinstance(Name, str))
      self.Name=Name
      
      assert(isinstance(Type, AccountType))
      self.Type=Type
      
      assert(isinstance(Owner, str))
      self.Owner=Owner
      
      assert(isinstance(Balance, int))
      self.Balance=Balance
      
      assert(isinstance(COLA, float))
      self.COLA=COLA
      
      self.AllocationPeriods=[]
      self.AssetClasses=[]
      
  def deposit(self, amount:float):
      assert(isinstance(amount, float))
      self.Balance+=amount
      
  def withdraw(self, amount:float):
      assert(isinstance(amount, float))
      self.Balance-=amount

  def calc_balance(self):
      self.Balance=self.Balance*(1.0 + self.COLA/100.0)
      return self.Balance
    
  def set_AllocationPeriods(self, periods):
      assert(len(periods) > 0)
      #sort periods by begin and end dates..
      self.AllocationPeriods=periods
      _mindate=date(2000, 1, 1)
      self.AllocationPeriods=sorted(periods, key=lambda x: x.BeginDate or _mindate)
  
  def set_AssetClasses(self, classes):
      assert(len(classes) > 0)
      
      self.AssetClasses=classes
      
  
  def calc_balance_by_year(self, year):
      #find the appropriate allocation period...
      _ap=self._get_correct_allocation_period(year)
      assert(isinstance(_ap, AllocationPeriod))
      
      _ac=self._get_assetclass_period(year)
      assert(isinstance(_ac, AssetClassPeriod))
      
      _balance_stocks=int(self.Balance*_ap.PercentStocks/100.0 * (1.0 + _ac.StockAssetClass.RateOfReturn/100.0))
      _balance_bonds=int(self.Balance*_ap.PercentBonds/100.0 * (1.0 + _ac.BondAssetClass.RateOfReturn/100.0))
      _balance_money_market=int(self.Balance*_ap.PercentMoneyMarket/100.0 * (1.0 + _ac.MoneyMarketAssetClass.RateOfReturn/100.0))
      
      self.Balance=_balance_stocks + _balance_bonds + _balance_money_market
      return self.Balance
      #print(allocation_period.PercentStocks, allocation_period.PercentBonds, allocation_period.PercentMoneyMarket)
      #print(asset_class.StockAssetClass.RateOfReturn, asset_class.StockAssetClass.StandardDeviation)
      
      
      
  def _get_correct_allocation_period(self, year):
      for _ap in self.AllocationPeriods:
          if _ap.BeginDate is None and _ap.EndDate is None:   #this period has no begin or end dated (ie, all years are valid)
              return _ap
          if _ap.BeginDate is None:   #no begin date (ie, begins at beginning of time)
              if year <= _ap.EndDate.year:
                 return _ap
          if _ap.EndDate is None:     #no end date (ie, ends at the end of time)
              if _ap.BeginDate.year <= year:
                 return _ap
          if _ap.BeginDate is not None and _ap.EndDate is not None:
              if _ap.BeginDate.year <= year <= _ap.EndDate.year:
                 return _ap 

  def _get_assetclass_period(self, year):
      for _ac in self.AssetClasses:
          if _ac.BeginDate is None and _ac.EndDate is None:   #this period has no begin or end dated (ie, all years are valid)
             return _ac
          if _ac.BeginDate is None:   #no begin date (ie, begins at beginning of time)
             if year <= _ac.EndDate.year:
                return _ac
          if _ac.EndDate is None:     #no end date (ie, ends at the end of time)
             if _ac.BeginDate.year <= year:
                return _ac
          if _ac.BeginDate is not None and _ac.EndDate is not None:
             if _ac.BeginDate.year <= year <= _ac.EndDate.year:
                return _ac
      
      print("An AssetClass for year '%s' has not been defined" % year)

class AllocationPeriod:
  def __init__(self, Name:str, BeginDate:date, EndDate:date, PercentStocks:float, PercentBonds:float, PercentMoneyMarket:float):
      
      assert(isinstance(Name, str))
      self.Name=Name
      
      assert(BeginDate is None or isinstance(BeginDate, date))
      self.BeginDate=BeginDate
      
      assert(EndDate is None or isinstance(EndDate, date))
      self.EndDate=EndDate
      
      assert(isinstance(PercentStocks, (int, float)))
      self.PercentStocks=PercentStocks
      
      assert(isinstance(PercentBonds, (int, float)))
      self.PercentBonds=PercentBonds
      
      assert(isinstance(PercentMoneyMarket, (int, float)))
      self.PercentMoneyMarket=PercentMoneyMarket
    
      #percent should add up to 100 (or pretty close)
      assert(99.0 < self.PercentStocks + self.PercentBonds + self.PercentMoneyMarket <= 100.0)
      
class AssetClass:
  def __init__(self, RateOfReturn:float, StandardDeviation:float):
      assert(isinstance(RateOfReturn, float))
      self.RateOfReturn=RateOfReturn

      assert(isinstance(StandardDeviation, float))
      self.StandardDeviation=StandardDeviation
      
class AssetClassPeriod:
  def __init__(self, StockAssetClass, BondAssetClass, MoneyMarketAssetClass, BeginDate=None, EndDate=None):
      assert(isinstance(StockAssetClass, AssetClass))
      self.StockAssetClass=StockAssetClass
      
      assert(isinstance(BondAssetClass, AssetClass))
      self.BondAssetClass=BondAssetClass
      
      assert(isinstance(MoneyMarketAssetClass, AssetClass))
      self.MoneyMarketAssetClass=MoneyMarketAssetClass
      
      assert(BeginDate is None or isinstance(BeginDate, date))
      self.BeginDate=BeginDate
             
      assert(EndDate is None or isinstance(EndDate, date))
      self.EndDate=EndDate
      
    