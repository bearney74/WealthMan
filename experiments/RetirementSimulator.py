import csv


class AllocationPeriod:
    def __init__(self, BeginYear, EndYear, pctStocks, pctBonds, pctCash):
        if BeginYear is None:
            self.BeginYear = 0
        else:
            self.BeginYear = BeginYear

        if EndYear is None:
            self.EndYear = 9999
        else:
            self.EndYear = EndYear

        assert self.BeginYear <= self.EndYear

        self.pctStocks = float(pctStocks) / 100.0
        self.pctBonds = float(pctBonds) / 100.0
        self.pctCash = float(pctCash) / 100.0

        _total = self.pctStocks + self.pctBonds + self.pctCash
        assert _total == 1.0


class AnnualReturnData:
    def __init__(self, Year, Stocks, Bonds, Cash, Inflation):
        self.Year = int(Year)
        self.Stocks = 1.0 + float(Stocks) / 100.0
        self.Bonds = 1.0 + float(Bonds) / 100.0
        self.Cash = 1.0 + float(Cash) / 100.0
        self.Inflation = 1.0 + float(Inflation) / 100.0


class HistoricalData:
    def __init__(self):
        self._data = []

        with open("asset_return_rates.csv", "r") as _fp:
            _csv = csv.reader(_fp)

            next(_csv)  # skip header
            next(_csv)  # skip header
            _dict={}
            for (
                _year,
                _sp500,
                _bond,
                _inflation,
            ) in _csv:
                _cash = 0.0  # cash has a return rate of 0
                _dict[int(_year)] = AnnualReturnData(
                    _year, _sp500, _bond, _cash, _inflation
                )

        #put data in self._data in year order (ie, sorted by year)
        _keys = list(_dict.keys())
        _keys.sort()
        for _key in _keys:
            self._data.append(_dict[_key])

        assert len(self._data) > 1


    def get_data(self, begin_year, end_year):
        _list = []

        for _record in self._data:
            # if _year is between begin_year and end_year:
            if _record.Year >= begin_year and _record.Year <= end_year:
                _list.append(_record)

        return _list


class BackTesting:
    def __init__(
        self,
        begin_year,
        end_year,
        incomes,
        expenses,
        accountBalance,
        accountAllocations,
        DefaultReturnRate=None,
    ):
        self.balance = accountBalance

        self.incomes = incomes
        self.expenses = expenses
        self.accountAllocations = accountAllocations
        self.defaultReturnRate = DefaultReturnRate

        _hd = HistoricalData()
        self._data = _hd.get_data(begin_year, end_year)

    def get_allocation_period(self, year):
        for _ap in self.accountAllocations:
            if _ap.BeginYear <= year and _ap.EndYear >= year:
                return _ap

        # we cannot find an appropriate allocation period or return None
        return None

    def execute(self):
        _success = True
        _inflation = 1.0
        for _record in self._data:
            _inflation *= _record.Inflation
            _year = _record.Year
            #add incomes to balance
            if _year in self.incomes:
                self.balance += self.incomes[_year]

            # we need to use inflation to adjust the expense values..
            if _year in self.expenses:
                self.balance -= self.expenses[_year] * _inflation

            # print(self.balance, _return)
            # find correct allocation
            _ap = self.get_allocation_period(_year)
            if _ap is None:
                print("AP is None")
                if self.defaultReturnRate is None:
                    print("DefaultReturnRate is None")
                    # log an error..
                    # send a message?
                else:
                    self.balance *= 1.0 + self.defaultReturnRate / 100.0
                    print("Using Default")
            else:  # we have a valid allocation Period..
                _balance = self.balance * _ap.pctStocks * _record.Stocks
                _balance += self.balance * _ap.pctBonds * _record.Bonds
                _balance += self.balance * _ap.pctCash * _record.Cash

                self.balance = _balance

            if self.balance <= 0:
                _success = False

        return _success, int(self.balance)


if __name__ == "__main__":

    def single_run(begin_year, end_year):
        balance = 100
        incomes = {}
        expenses = {}

        allocationPeriods = [
           # AllocationPeriod(1928, 2000, 80, 15, 5),
           # AllocationPeriod(2001, None, 80, 15, 5),
            AllocationPeriod(1928, None, 80, 20, 0),
        ]

        for _i in range(begin_year, end_year + 1):
            expenses[_i] = 4

        _rs = BackTesting(
            begin_year,
            end_year,
            incomes,
            expenses,
            balance,
            allocationPeriods,
            DefaultReturnRate=5.0,
        )
        _success, _balance = _rs.execute()
        return _success, _balance

    # single_run(2000, 2010)
    # single_run(2001, 2011)
    _count=0
    _total=0
    for _begin_year in range(1928, 2025 - 30 + 1):
        _success, _balance=single_run(_begin_year, _begin_year + 30)
        _total+=1
        if _success:
            _count+=1

    print("Success: %4.2f%%" % (100.0*_count/_total))