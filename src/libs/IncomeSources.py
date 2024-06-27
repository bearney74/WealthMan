from datetime import date

from .EnumTypes import IncomeSourceType, AmountPeriodType, AccountOwnerType
from .IncomeExpenseBase import IncomeExpenseBase


class IncomeSource(IncomeExpenseBase):
    def __init__(
        self,
        Name: str,
        IncomeType: IncomeSourceType,
        Amount: int,
        AmountPeriod: AmountPeriodType,
        Owner: AccountOwnerType,
        BirthDate: date,
        BeginAge: int = None,
        LifeSpanAge: int=None,
        SurvivorPercent: float = 0.0,
        Taxable: bool = None,
        COLA: float = 0,
    ):
        super(IncomeSource, self).__init__(
            Name=Name, Amount=Amount, AmountPeriod=AmountPeriod,
            BirthDate=BirthDate,
            BeginAge=BeginAge, LifeSpanAge=LifeSpanAge,
            SurvivorPercent=SurvivorPercent, COLA=COLA
        )
        assert isinstance(IncomeType, IncomeSourceType)
        self.IncomeType = IncomeType

        assert isinstance(Owner, AccountOwnerType) or Owner is None
        self.Owner = Owner

        if LifeSpanAge is None:
            self.LifeSpanDate=None
        else:
            self.LifeSpanDate=date(BirthDate.year + LifeSpanAge, BirthDate.month, BirthDate.day)

        self.SurvivorPercent = SurvivorPercent
        self.Taxable = Taxable

    def calc_balance_by_year(self, year):
        _balance=IncomeExpenseBase.calc_balance_by_year(self, year)

        if self.LifeSpanDate is not None and self.LifeSpanDate.year < year:
            return int(self.SurvivorPercent/100.0 * _balance)
     
        #if we get here, #we are single, or #spouse is still alive
        return _balance

class SocialSecurity(IncomeSource):
    def __init__(
        self,
        Name: str,
        BirthDate: date,
        FRAAmount: int,
        Owner: AccountOwnerType,
        BeginAge: int=None,
        LifeSpanAge: int = None,
        COLA: float = 0,
    ):
        #table used to figure out the SS benefit based on Age benefits start...
        self._table: dict[int, float] = {
            62: 0.7,
            63: 0.75,
            64: 0.80,
            65: 0.866667,
            66: 0.933333,
            67: 1.0,
            68: 1.08,
            69: 1.16,
            70: 1.24,
        }

        self.FRAAmount=FRAAmount
        #todo: need to calculate Amount from FRAAmount and birthdate...
        assert BeginAge in self._table.keys()
        Amount=int(self.FRAAmount * self._table[BeginAge])

        
        self.SpouseObj=None

        super(SocialSecurity, self).__init__(
            Name=Name,
            IncomeType=IncomeSourceType.SocialSecurity,
            Amount=Amount,
            AmountPeriod=AmountPeriodType.Annual,
            Owner=Owner,
            BirthDate=BirthDate,
            BeginAge=BeginAge,
            LifeSpanAge=LifeSpanAge,
            COLA=COLA
        )
        
    def set_SpouseSS(self, SpouseObj):
        #assert isinstance(SpouseObj, SocialSecurity)
        
        self.SpouseObj=SpouseObj
        
    def IamDead(self, year) -> bool:
        return self.LifeSpanDate.year < year
    
    def calc_balance_by_year(self, year) -> int:
    
        if year > self.LifeSpanDate.year:
            return 0   #assume we are dead..
        
        #we are alive.. what about spouse?
        if self.SpouseObj is not None:
            if self.SpouseObj.IamDead(year):
                return max(self.SpouseObj.calc_balance_by_year_for_SpouseBenefit(year),
                           IncomeSource.calc_balance_by_year(self, year))
            
        #if we get here, #we are single, or #spouse is still alive
        return IncomeSource.calc_balance_by_year(self, year)
    
    def calc_balance_by_year_for_SpouseBenefit(self, year):
        return IncomeSource.calc_balance_by_year(self, year)