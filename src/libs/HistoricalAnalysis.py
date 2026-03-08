import os
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
        assert pctStocks >= 0
        assert pctBonds >= 0
        assert pctCash >= 0

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
        self.Inflation = (
            float(Inflation) / 100.0
        )  # sometimes we add this (expenses) sometimes subtract (balance)


class HistoricalData:
    def __init__(self):
        self._data = []

        # print(__file__)
        # import os
        # print(os.getcwd())
        _filename = "data/asset_return_rates.csv"
        if not os.path.exists(_filename):
            _filename = "src/libs/data/asset_return_rates.csv"

        with open(_filename, "r") as _fp:
            _csv = csv.reader(_fp)

            next(_csv)  # skip header
            next(_csv)  # skip header
            _dict = {}
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

        # put data in self._data in year order (ie, sorted by year)
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


class HistoricalAnalysis:
    def __init__(
        self,
        begin_year,
        end_year,
        incomes_fixed,
        incomes_with_COLA,
        expenses,
        accountBalance,
        accountAllocations,
        DefaultReturnRate=None,
    ):
        self._balances = []
        self._balance = accountBalance

        self._incomes_fixed = incomes_fixed
        self._incomes_with_COLA = incomes_with_COLA
        self._expenses = expenses
        self._accountAllocations = accountAllocations
        self._defaultReturnRate = DefaultReturnRate

        _hd = HistoricalData()
        self._data = _hd.get_data(begin_year, end_year)

        # print(len(incomes_fixed), len(incomes_with_COLA), len(expenses), len(self._data))
        assert (
            len(incomes_fixed)
            == len(incomes_with_COLA)
            == len(expenses)
            == len(self._data)
        )

    def get_allocation_period(self, year):
        for _ap in self._accountAllocations:
            if _ap.BeginYear <= year and _ap.EndYear >= year:
                return _ap

        # we cannot find an appropriate allocation period or return None
        return None

    def execute(self):
        self._balances = [self._balance]
        _success = True
        # _inflation = 1.0
        for _pos, _record in enumerate(self._data):
            self._balance += self._incomes_fixed[_pos]
            self._balance += self._incomes_with_COLA[_pos] * (1.0 + _record.Inflation)
            self._balance -= self._expenses[_pos] * (1.0 + _record.Inflation)

            # print(self.balance, _return)
            # find correct allocation
            _ap = self.get_allocation_period(_pos)
            if _ap is None:
                print("AP is None pos=%s" % _pos)
                if self._defaultReturnRate is None:
                    print("DefaultReturnRate is None")
                    # log an error..
                    # send a message?
                else:
                    self._balance *= 1.0 + self._defaultReturnRate / 100.0
                    print("Using Default")
            else:  # we have a valid allocation Period..
                _balance = self._balance * _ap.pctStocks * _record.Stocks
                _balance += self._balance * _ap.pctBonds * _record.Bonds
                _balance += self._balance * _ap.pctCash * _record.Cash

                self._balance = _balance * (1.0 - _record.Inflation)

            if self._balance <= 0:
                _success = False

            self._balances.append(self._balance)

        return _success, self._balances

    def get_balances(self):
        return self._balance


if __name__ == "__main__":

    def single_run(begin_year, end_year):
        balance = 100
        incomes_fixed = []
        incomes_with_COLA = []
        expenses = []

        allocationPeriods = [
            AllocationPeriod(0, 10, 80, 15, 5),
            AllocationPeriod(11, 20, 70, 25, 5),
            AllocationPeriod(20, None, 60, 40, 0),
        ]

        for _i in range(begin_year, end_year + 1):
            incomes_fixed.append(0)
            incomes_with_COLA.append(0)
            expenses.append(4)

        _rs = HistoricalAnalysis(
            begin_year,
            end_year,
            incomes_fixed,
            incomes_with_COLA,
            expenses,
            balance,
            allocationPeriods,
            DefaultReturnRate=5.0,
        )
        _success, _balance = _rs.execute()
        return _success, _balance

    # single_run(2000, 2010)
    # single_run(2001, 2011)
    _count = 0
    _total = 0
    _num_years = 25
    for _begin_year in range(1928, 2025 - _num_years + 1):
        _success, _balance = single_run(_begin_year, _begin_year + _num_years)
        _total += 1
        if _success:
            _count += 1

    print("Success: %4.2f%%" % (100.0 * _count / _total))
