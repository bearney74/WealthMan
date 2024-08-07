from datetime import date

from .EnumTypes import AccountType, AccountOwnerType


class Account:
    def __init__(
        self,
        Name: str,
        Type: AccountType,
        Owner: AccountOwnerType,
        BirthDate: date = None,
        Balance: int = 0,
        Contribution: int = 0,
        ContributionBeginAge: int = None,
        ContributionEndAge: int = None,
        COLA: float = 0.0,
    ):
        assert isinstance(Name, str)
        self.Name = Name

        assert isinstance(Type, AccountType)
        self.Type = Type

        assert isinstance(Owner, AccountOwnerType)
        self.Owner = Owner

        assert isinstance(Balance, int)
        self._balance = Balance

        assert isinstance(COLA, float)
        if abs(COLA) >= 1:
            self.COLA = 1.0 + COLA / 100.0
        else:
            self.COLA = 1.0 + COLA

        if Contribution is None:
            Contribution = 0
        self.Contribution = Contribution
        if ContributionBeginAge is None:
            ContributionBeginAge = 0
        if ContributionEndAge is None:
            ContributionEndAge = 99

        if BirthDate is not None:
            assert isinstance(BirthDate, date)
            self.ContributionBeginDate = date(
                BirthDate.year + ContributionBeginAge, BirthDate.month, BirthDate.day
            )
            self.ContributionEndDate = date(
                BirthDate.year + ContributionEndAge, BirthDate.month, BirthDate.day
            )
        else:
            self.ContributionBeginDate = None
            self.ContributionEndDate = None

    @property
    def Balance(self):
        return self._balance

    @Balance.setter
    def Balance(self, amount):
        self._balance = amount

    def deposit(self, amount: int):
        assert isinstance(amount, int)
        self._balance += amount

    def withdraw(self, amount: int):
        assert isinstance(amount, int)
        self._balance -= amount

    def calc_balance(self, year=None):
        if self._balance > 0:
            self._balance = int(self._balance * self.COLA)

        if (
            self.Contribution > 0
            and year is not None
            and year >= self.ContributionBeginDate.year
            and year <= self.ContributionEndDate.year
        ):
            self._balance += self.Contribution
            return self._balance, self.Contribution

        return self._balance, 0


##  maybe implement Allocation Periods sometime in the future??
# todo delete stuff below this line
"""
    def set_AllocationPeriods(self, periods):
        assert len(periods) > 0
        # sort periods by begin and end dates..
        self.AllocationPeriods = periods
        _mindate = date(2000, 1, 1)
        self.AllocationPeriods = sorted(periods, key=lambda x: x.BeginDate or _mindate)

    def set_AssetClasses(self, classes):
        assert len(classes) > 0

        self.AssetClasses = classes

    def calc_balance_by_year(self, year) -> int:
        # find the appropriate allocation period...
        if self.COLA is not None:
            self.Balance *= 1.0 + self.COLA / 100.0
            return int(self.Balance)

        _ap = self._get_correct_allocation_period(year)
        assert isinstance(_ap, AllocationPeriod)

        _ac = self._get_assetclass_period(year)
        assert isinstance(_ac, AssetClassPeriod)

        _balance_stocks = int(
            self.Balance
            * _ap.PercentStocks
            / 100.0
            * (1.0 + _ac.StockAssetClass.RateOfReturn / 100.0)
        )
        _balance_bonds = int(
            self.Balance
            * _ap.PercentBonds
            / 100.0
            * (1.0 + _ac.BondAssetClass.RateOfReturn / 100.0)
        )
        _balance_money_market = int(
            self.Balance
            * _ap.PercentMoneyMarket
            / 100.0
            * (1.0 + _ac.MoneyMarketAssetClass.RateOfReturn / 100.0)
        )

        self.Balance = _balance_stocks + _balance_bonds + _balance_money_market
        return self.Balance
        
    def _get_correct_allocation_period(self, year):
        for _ap in self.AllocationPeriods:
            if (
                _ap.BeginDate is None and _ap.EndDate is None
            ):  # this period has no begin or end dated (ie, all years are valid)
                return _ap
            if _ap.BeginDate is None:  # no begin date (ie, begins at beginning of time)
                if year <= _ap.EndDate.year:
                    return _ap
            if _ap.EndDate is None:  # no end date (ie, ends at the end of time)
                if _ap.BeginDate.year <= year:
                    return _ap
            if _ap.BeginDate is not None and _ap.EndDate is not None:
                if _ap.BeginDate.year <= year <= _ap.EndDate.year:
                    return _ap

        assert False, "We don't have a valid allocation period for year %s" % year

    def _get_assetclass_period(self, year):
        for _ac in self.AssetClasses:
            if (
                _ac.BeginDate is None and _ac.EndDate is None
            ):  # this period has no begin or end dated (ie, all years are valid)
                return _ac
            if _ac.BeginDate is None:  # no begin date (ie, begins at beginning of time)
                if year <= _ac.EndDate.year:
                    return _ac
            if _ac.EndDate is None:  # no end date (ie, ends at the end of time)
                if _ac.BeginDate.year <= year:
                    return _ac
            if _ac.BeginDate is not None and _ac.EndDate is not None:
                if _ac.BeginDate.year <= year <= _ac.EndDate.year:
                    return _ac

        print("An AssetClass for year '%s' has not been defined" % year)


class AllocationPeriod:
    def __init__(
        self,
        Name: str,
        BeginDate: date,
        EndDate: date,
        PercentStocks: float,
        PercentBonds: float,
        PercentMoneyMarket: float,
    ):
        assert isinstance(Name, str)
        self.Name = Name

        assert BeginDate is None or isinstance(BeginDate, date)
        self.BeginDate = BeginDate

        assert EndDate is None or isinstance(EndDate, date)
        self.EndDate = EndDate

        assert isinstance(PercentStocks, (int, float))
        self.PercentStocks = PercentStocks

        assert isinstance(PercentBonds, (int, float))
        self.PercentBonds = PercentBonds

        assert isinstance(PercentMoneyMarket, (int, float))
        self.PercentMoneyMarket = PercentMoneyMarket

        # percent should add up to 100 (or pretty close)
        assert (
            99.0
            < self.PercentStocks + self.PercentBonds + self.PercentMoneyMarket
            <= 100.0
        )


class AssetClass:
    def __init__(self, RateOfReturn: float, StandardDeviation: float):
        assert isinstance(RateOfReturn, float)
        self.RateOfReturn = RateOfReturn

        assert isinstance(StandardDeviation, float)
        self.StandardDeviation = StandardDeviation


class AssetClassPeriod:
    def __init__(
        self,
        StockAssetClass,
        BondAssetClass,
        MoneyMarketAssetClass,
        BeginDate=None,
        EndDate=None,
    ):
        assert isinstance(StockAssetClass, AssetClass)
        self.StockAssetClass = StockAssetClass

        assert isinstance(BondAssetClass, AssetClass)
        self.BondAssetClass = BondAssetClass

        assert isinstance(MoneyMarketAssetClass, AssetClass)
        self.MoneyMarketAssetClass = MoneyMarketAssetClass

        assert BeginDate is None or isinstance(BeginDate, date)
        self.BeginDate = BeginDate

        assert EndDate is None or isinstance(EndDate, date)
        self.EndDate = EndDate

"""
