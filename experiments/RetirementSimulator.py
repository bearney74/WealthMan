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
    def __init__(self, Year, Stocks, Bonds, Cash):
        self.Year = int(Year)
        self.Stocks = 1.0 + float(Stocks) / 100.0
        self.Bonds = 1.0 + float(Bonds) / 100.0
        self.Cash = 1.0 + float(Cash) / 100.0


class HistoricalData:
    def __init__(self):
        self._data = {}

        with open("history.csv", "r") as _fp:
            _csv = csv.reader(_fp)

            next(_csv)  # skip header
            for (
                _year,
                _sp500,
                _bond,
                _cash,
            ) in _csv:
                self._data[int(_year)] = AnnualReturnData(_year, _sp500, _bond, _cash)

        assert len(self._data) > 1

        self._data = dict(sorted(self._data.items()))

    def get_data(self, begin_year, end_year):
        _list = []

        for _year, _ard in self._data.items():
            if _year >= begin_year and _year <= end_year:
                _list.append((_year, _ard))

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
        for _year, _ard in self._data:
            if _year in self.incomes:
                self.balance += self.incomes[_year]

            if _year in self.expenses:
                self.balance -= self.expenses[_year]

            # print(self.balance, _return)
            # find correct allocation
            _ap = self.get_allocation_period(_year)
            if _ap is None:
                if self.DefaultReturnRate is None:
                    print("DefaultReturnRate is None")
                    # log an error..
                    # send a message?
                else:
                    self.balance *= 1.0 + self.DefaultReturnRate / 100.0
            else:  # we have a valid allocation Period..
                _balance = self.balance * _ap.pctStocks * _ard.Stocks
                _balance += self.balance * _ap.pctBonds * _ard.Bonds
                _balance += self.balance * _ap.pctCash * _ard.Cash

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
            AllocationPeriod(1926, 2000, 50, 25, 25),
            AllocationPeriod(2001, None, 75, 20, 5),
        ]

        for _i in range(begin_year, end_year + 1):
            expenses[_i] = 5

        _rs = BackTesting(
            begin_year,
            end_year,
            incomes,
            expenses,
            balance,
            allocationPeriods,
            DefaultReturnRate=5.0,
        )
        print("%s->%s: %s, %s" % tuple((begin_year, end_year) + _rs.execute()))

    # single_run(2000, 2010)
    # single_run(2001, 2011)
    for _begin_year in range(1926, 2023 - 30 + 1):
        single_run(_begin_year, _begin_year + 30)
