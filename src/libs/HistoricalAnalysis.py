import os
import csv

from .Projections import DataItem


class PeriodData:
    def __init__(self, beginYear: int, endYear: int):
        assert isinstance(beginYear, int)
        assert isinstance(endYear, int)
        assert beginYear <= endYear
        self.Period = DataItem("Period", "{}", "%s-%s" % (beginYear, endYear))

        self.EndingBalance = DataItem("Ending Balance")
        self.Success = DataItem("Successful Period", "{}", True)
        self.BankruptYear = DataItem("Bankrupt Year", "{:}", None)


class DetailedPeriodData:
    def __init__(self, beginYear: int, endYear: int, currentYear: int):
        assert isinstance(beginYear, int)
        assert isinstance(endYear, int)
        assert beginYear <= endYear
        self.period = DataItem("Period", "{}", "%s-%s" % (beginYear, endYear))

        assert isinstance(currentYear, int)
        self.currentYear = DataItem("Current Year", "{}", currentYear)

        # maybe uncomment when we have more than one allocation
        # self.PctStocks = DataItem("% Stocks", "{:.1f}%", 0.0)
        # self.PctBonds = DataItem("% Bonds", "{:.1f}%", 0.0)
        # self.PctCash = DataItem("% Cash", "{:.1f}%", 0.0)

        self.StockReturns = DataItem("Stock Returns", "{:.2f}%", 0.0)
        self.BondReturns = DataItem("Bond Returns", "{:.2f}%", 0.0)
        self.CashReturns = DataItem("Cash Returns", "{:.2f}%", 0.0)
        self.InflationRate = DataItem("Inflation Rate", "{:.2f}%", 0.0)

        self.RORStocks = DataItem("Stocks ROR", "{:.2f}%", 0.0)
        self.RORBonds = DataItem("Bonds ROR", "{:.2f}%", 0.0)
        self.RORCash = DataItem("Cash ROR", "{:.2f}%", 0.0)

        self.PreBalance = DataItem("Pre Balance")
        self.FixedIncome = DataItem("Fixed Income")
        self.FixedIncomeInflationAdjusted = DataItem("Fixed Income Inflation Adjusted")
        self.ColaIncome = DataItem("COLA Income")  # will adjust to inflation
        # self.ColaIncomeInflation = DataItem("COLA Income Inflation")
        self.Expenses = DataItem("Expenses")  # will adjust to inflation
        # self.ExpenseInflation = DataItem("Expense Inflation")

        self.NetIncome = DataItem("Net Income")
        self.BalancePostNetIncome = DataItem("Balance Post Net Income")

        self.StocksBalance = DataItem("Stocks Balance")
        self.BondsBalance = DataItem("Bonds Balance")
        self.CashBalance = DataItem("Cash Balance")

        # balance at the beginning of the period
        self.Inflation = DataItem("Inflation")  # inflation balance for the year
        self.PostBalance = DataItem("Post Balance")  # balance at the end of the period


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
        assert pctStocks + pctBonds + pctCash == 100

        self.pctStocks = float(pctStocks) / 100.0
        self.pctBonds = float(pctBonds) / 100.0
        self.pctCash = float(pctCash) / 100.0


class AnnualReturnData:
    def __init__(self, Year, Stocks, Bonds, Cash, Inflation):
        self.Year = int(Year)

        self.Stocks = float(Stocks) / 100.0
        self.Bonds = float(Bonds) / 100.0
        self.Cash = float(Cash) / 100.0
        self.Inflation = float(Inflation) / 100.0


class HistoricalData:
    def __init__(self):
        self._data = []
        self.firstYear = 9999
        self.lastYear = 0

        self._read_file()

    def _read_file(self):
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
                self.firstYear = min(self.firstYear, int(_year))
                self.lastYear = max(self.lastYear, int(_year))
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
        historicalData,
        begin_year,
        end_year,
        incomes_fixed,
        incomes_with_COLA,
        expenses,
        accountBalance,
        accountAllocations,
        DefaultReturnRate=None,
    ):
        self._begin_year = begin_year
        self._end_year = end_year
        self._periodData: [
            DetailedPeriodData
        ] = []  # contains the data we put on the gui table

        self._balances = []
        self._balance = accountBalance

        self._incomes_fixed = incomes_fixed
        self._incomes_with_COLA = incomes_with_COLA
        self._expenses = expenses
        self._accountAllocations = accountAllocations
        self._defaultReturnRate = DefaultReturnRate

        self._data = historicalData.get_data(begin_year, end_year - 1)

        assert (
            len(incomes_fixed)
            == len(incomes_with_COLA)
            == len(expenses)
            == len(self._data)
        ), (
            "len(incomes_fixed) = %s, len(incomes_with_COLA) = %s, len(expenses) = %s, len(self._data) = %s"
            % (
                len(incomes_fixed),
                len(incomes_with_COLA),
                len(expenses),
                len(self._data),
            )
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
        _bankrupt_year = None
        _accInflation = 1.0
        _pds = []
        for _pos, _record in enumerate(self._data):
            _pd = DetailedPeriodData(
                self._begin_year, self._end_year, self._begin_year + _pos
            )
            _accInflation = _accInflation * (1.0 - _record.Inflation)

            _pd.StockReturns.data = _record.Stocks * 100.0
            _pd.BondReturns.data = _record.Bonds * 100.0
            _pd.CashReturns.data = _record.Cash * 100.0

            _pd.InflationRate.data = 100.0 * _record.Inflation
            _pd.FixedIncome.data = self._incomes_fixed[_pos]
            _pd.FixedIncomeInflationAdjusted.data = int(
                self._incomes_fixed[_pos] * _accInflation
            )
            _pd.ColaIncome.data = self._incomes_with_COLA[_pos]
            _pd.Expenses.data = self._expenses[_pos]
            _pd.PreBalance.data = self._balance

            _pd.NetIncome.data = (
                _pd.FixedIncomeInflationAdjusted.data
                + _pd.ColaIncome.data
                - _pd.Expenses.data
            )

            self._balance += _pd.NetIncome.data
            _pd.BalancePostNetIncome.data = self._balance

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
                _pd.RORStocks.data = 100.0 * (_record.Stocks - _record.Inflation)
                _pd.RORBonds.data = 100.0 * (_record.Bonds - _record.Inflation)
                _pd.RORCash.data = 100.0 * (_record.Cash - _record.Inflation)
                # _pd.PctStocks.data = 100.0 * _ap.pctStocks
                # _pd.PctBonds.data = 100.0 * _ap.pctBonds
                # _pd.PctCash.data = 100.0 * _ap.pctCash

                _pd.StocksBalance.data = int(
                    self._balance * _ap.pctStocks * (1.0 + _pd.RORStocks.data / 100.0)
                )
                _pd.BondsBalance.data = int(
                    self._balance * _ap.pctBonds * (1.0 + _pd.RORBonds.data / 100.0)
                )
                _pd.CashBalance.data = int(
                    self._balance * _ap.pctCash * (1.0 + _pd.RORCash.data / 100.0)
                )

                self._balance = (
                    _pd.StocksBalance.data
                    + _pd.BondsBalance.data
                    + _pd.CashBalance.data
                )

            _pd.Inflation.data = int(self._balance * _record.Inflation)
            self._balance -= _pd.Inflation.data
            _pd.PostBalance.data = self._balance

            _pds.append(_pd)
            if self._balance <= 0:
                _success = False
                if _bankrupt_year is None:
                    _bankrupt_year = _pos

            self._balances.append(self._balance)

        _p = PeriodData(self._begin_year, self._end_year)
        _p.EndingBalance.data = self._balance
        _p.Success.data = _success
        _p.BankruptYear.data = "-" if _bankrupt_year is None else _bankrupt_year

        return _success, self._balances, _p, _pds

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

        _historicalData = HistoricalData()
        _rs = HistoricalAnalysis(
            _historicalData,
            begin_year,
            end_year,
            incomes_fixed,
            incomes_with_COLA,
            expenses,
            balance,
            allocationPeriods,
            DefaultReturnRate=5.0,
        )
        _success, _balance, _pd = _rs.execute()
        return _success, _balance, _pd

    # single_run(2000, 2010)
    # single_run(2001, 2011)
    _count = 0
    _total = 0
    _num_years = 25
    _period_data = []
    for _begin_year in range(1928, 2025 - _num_years + 1):
        _success, _balance, _pd = single_run(_begin_year, _begin_year + _num_years)
        _period_data.append(_pd)
        _total += 1
        if _success:
            _count += 1

    print("Success: %4.2f%%" % (100.0 * _count / _total))
