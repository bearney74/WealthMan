import csv
# import datetime

from enum import Enum


class WithdrawType(Enum):
    FLAT = (
        0  # set withdraw amount over the years ($50K in year 2025, $50K in year 2050)
    )
    INFLATION = 1  # withdraw increases with inflation
    RAILING = 2  # railing type (maybe between 3 and 5 % of full balance)


class WithdrawTimingType(Enum):
    BEFORE = 0  # withdraw from account before doing return calculations.
    AFTER = 1  # withdraw from account after doing return calculations.


class BasicWithdrawObj:
    def __init__(
        self, amount: float, inflation: float, withdrawTimingType: WithdrawTimingType
    ):
        assert isinstance(amount, float)
        self._amount = amount

        assert isinstance(inflation, float)
        self._inflation = inflation / 100.0

        # assert isinstance(withdrawType, WithdrawType)
        # self.WithdrawType=withdrawType

        assert isinstance(withdrawTimingType, WithdrawTimingType)
        self.withdrawTimingType = withdrawTimingType

        self._count = -1

        self._withdraws = []

    # @property
    # def WithdrawType(self):
    #    return self.WithdrawType

    @property
    def WithdrawTimingType(self):
        return self.withdrawTimingType

    def reset(self):
        self._count = -1
        self._withdraws = []

    def step(self):
        self._count += 1

    def factor(self):
        return pow(1.0 + self._inflation, self._count)

    def amount(self, balance):  # we don't need balance for this obj, but is needed for
        # RailingWithdrawObj..
        _amt = self._amount * self.factor()
        self._withdraws.append(_amt)
        return _amt

    def get_withdraws(self):
        return self._withdraws


class GuardRailWithdrawObj(BasicWithdrawObj):
    def __init__(
        self,
        amount: float,
        inflation: float,
        top_percent: float,
        bottom_percent: float,
        withdraw_timing: WithdrawTimingType = WithdrawTimingType.AFTER,
    ):
        BasicWithdrawObj.__init__(self, amount, inflation, withdraw_timing)

        assert isinstance(top_percent, float)
        self._top_percent = top_percent / 100.0

        assert isinstance(top_percent, float)
        self._bottom_percent = bottom_percent / 100.0

    def amount(self, balance):
        # print(balance)
        _amt = self._amount * BasicWithdrawObj.factor(self)
        _upper = balance * (self._top_percent)
        # _top=self._amount*pow(1.0+self._top_percent, self._count)
        # print("top:", _amt, _upper)
        # print(balance, self._top_percent)
        _lower = balance * (self._bottom_percent)

        _withdraw = min(max(_amt, _lower), _upper)
        self._withdraws.append(_withdraw)
        return _withdraw
        # market is underperforming...
        # expected withdraw > upper percent of account balance
        if _amt > _upper:
            _bottom = self._amount * pow(1.0 + self._bottom_percent, self._count)
            print("Top:Using %s instead of %s" % (_bottom, _amt))
            self._withdraws.append(_bottom)
            return _bottom

        # _lower=balance * (self._bottom_percent)
        # _bottom=self._amount*pow(1.0+self._bottom_percent, self._count)
        print("bottom:", _amt, _lower)

        # market is overperforming..
        # expected withdraw is less than lower percent of account balance
        if _amt < _lower:
            _top = self._amount * pow(1.0 + self._top_percent, self._count)
            print("Bottom:Using %s instead of %s" % (_top, _amt))
            self._withdraws.append(_top)
            return _top
            # return _lower

        # we are within our bounds so just return the amount
        print("Using amount: %s" % _amt)
        self._withdraws.append(_amt)
        return _amt


class MonthlyDataObj:
    def __init__(self, filename):
        self._data = {}
        self._filename = filename

    def get_date_data(self, year, month=1):
        _date = "%04d-%02d-01" % (year, month)

        assert _date in self._data, "file '%s' does not contain a date for '%s'" % (
            self._filename,
            _date,
        )

        return self._data[_date]

    def _get_data(self, filename):
        """data must be in csv file with each row containing three values (date, value, percent_change)"""

        with open(filename, "r") as f:
            _csv = csv.reader(f)
            for (
                _date,
                value,
                _percent,
            ) in _csv:
                self._data[_date] = float(_percent)


class YearlyDataObj:
    def __init__(self, filename):
        self._data = {}
        self._filename = filename
        self._get_data(filename)

    def get_date_data(self, year):
        _date = "%04d" % (year)
        assert _date in self._data, "file '%s' does not contain a date for '%s'" % (
            self._filename,
            _date,
        )

        return self._data[_date]

    def _get_data(self, filename):
        """data must be in csv file with each row containing three values (date, value, percent_change)"""

        with open(filename, "r") as f:
            _csv = csv.reader(f)
            for (
                _date,
                _returns,
            ) in _csv:
                self._data[_date] = float(_returns)


class BasicSimulator:
    def __init__(
        self,
        balance: float,
        withdrawObj: BasicWithdrawObj,
        # withdraw_amount:float, withdraw_inflation: float,
        start_year: int,
        length_in_years: int,
        # withdraw_timing:WithdrawType
    ):
        assert isinstance(balance, float)
        self._balance = balance

        assert isinstance(withdrawObj, BasicWithdrawObj)
        self._withdrawObj = withdrawObj
        # assert isinstance(withdraw_amount, float)
        # self._withdraw_amount=withdraw_amount

        # assert isinstance(withdraw_inflation, float)
        # self._withdraw_inflation=withdraw_inflation

        # assert isinstance(withdraw_timing, WithdrawType)
        # self._withdraw_timing=withdraw_timing

        assert isinstance(start_year, int)
        self._start_year = start_year

        assert isinstance(length_in_years, int)
        self._length = length_in_years

        self._bankrupt = None
        self._values = {}

        self._data = None  # we will use the set_data function to set this value..

    def set_data(self, data):
        # should use the get_data function to retrieve data from a csv file and populate the self._data field
        self._data = data

    def get_simulation_values(self):
        """return monthly balance of account for each month in the simulation"""
        return self._values

    def is_bankrupt(self):
        return self._bankrupt

    def process(self):
        assert self._data is not None, "Error, must set data variable before processing"

        self._bankrupt = False

    def get_withdraw_values(self):
        return self._withdrawObj.get_withdraws()

    # make a better name for this...
    # def withdraw_step(self, balance):


class BasicMonthlySimulator(BasicSimulator):
    def __init__(
        self,
        balance,
        monthly_withdraw,
        start_year,
        start_month,
        length_in_years=30,
        withdraw_timing=WithdrawTimingType.BEFORE,
    ):
        BasicSimulator.__init__(
            self,
            balance,
            monthly_withdraw,
            start_year,
            length_in_years,
            withdraw_timing=withdraw_timing,
        )
        self._start_month = start_month

    def set_data(self, data):
        assert isinstance(data, MonthlyDataObj)
        BasicSimulator.set_data(self, data)

    def process(self):
        BasicSimulator.process(self)
        _value = self._balance

        self._withdrawObj.reset()  # can reuse the same withdraw object...

        _end_year = self._start_year + self._length
        for _year in range(self._start_year, _end_year + 1):
            for _month in range(1, 13):
                # look for months outside our range and skip those..
                if _year == self._start_year and _month < self._start_month:
                    continue  # we can skip this month since it is out of range...
                if _year == _end_year and _month > self._start_month:
                    continue  # we can skip this month since it is out of range...

                _date = "%04d-%02d-01" % (_year, _month)

                if (
                    self._bankrupt
                ):  # no need to do calcs below since we have no money left :(
                    self._values[_date] = 0.0
                    continue

                self._withdrawObj.step()

                if self._withdrawObj.WithdrawTimingType == WithdrawTimingType.BEFORE:
                    _value -= self._withdrawObject.value(_value)

                _value *= (100.0 + self._data.get_date_data(_year, _month)) / 100.0

                if self._withdrawObj.WithdrawTimingType == WithdrawTimingType.AFTER:
                    _value -= self._withdrawObject.value(_value)

                if _value > 0.0:
                    self._values[_date] = round(_value, 2)
                    # _old_value=_value
                else:  # we have no money left.  this simulation is a failure.. :(
                    self._bankrupt = True
                    self._values[_date] = 0.0


class YearlySimulator(BasicSimulator):
    def __init__(self, balance, withdraw_obj, start_year, length_in_years=30):
        BasicSimulator.__init__(
            self, balance, withdraw_obj, start_year, length_in_years
        )

    def set_data(self, data):
        assert isinstance(data, YearlyDataObj)
        BasicSimulator.set_data(self, data)

    def process(self):
        BasicSimulator.process(self)
        _value = self._balance
        self._withdrawObj.reset()

        _end_year = self._start_year + self._length
        for _year in range(self._start_year, _end_year + 1):
            _date = "%04d" % (_year)

            # print(self._bankrupt)
            if (
                self._bankrupt
            ):  # no need to do calcs below since we have no money left :(
                self._values[_date] = 0.0
                continue

            # print(_date)
            self._withdrawObj.step()

            # print(self._withdrawObj.amount(_value))
            if self._withdrawObj.WithdrawTimingType == WithdrawTimingType.BEFORE:
                _value -= self._withdrawObj.amount(_value)

            _value *= (100.0 + self._data.get_date_data(_year)) / 100.0

            if self._withdrawObj.WithdrawTimingType == WithdrawTimingType.AFTER:
                _value -= self._withdrawObj.amount(_value)

            if _value > 0.0:
                self._values[_date] = round(_value, 2)
                _old_value = _value
            else:  # we have no money left.  this simulation is a failure.. :(
                self._bankrupt = True
                self._values[_date] = 0.0


def stats(data):
    import statistics as st
    from math import fsum

    return {
        "min": min(data),
        "max": max(data),
        "sum": fsum(data),
        "mean": st.mean(data),
        "median": st.median(data),
        "std dev": st.stdev(data),
        "last": data[-1],
    }


_data = YearlyDataObj("sp500_yearly_returns.csv")
# print(_data)

## variables
## amount of account
## withdraw amount (or percentage 4.0%)
## inflation
## withdraw amount before/after calculating returns
## number of years to do prediction on (30 year, 40 years)


_withdraw_obj = BasicWithdrawObj(40.0, 3.0, WithdrawTimingType.AFTER)

# _withdraw_obj=GuardRailWithdrawObj(1000 * 0.04, 3.0, 5.0, 3.0)

# if 0:
_out = csv.writer(open("out1.csv", "w"))
for _year in range(1926, 1985):
    # print(_year)
    # for _month in range(1,13):
    # _ys=YearlySimulator(1000.00, 40.0, 3.0, _year, 30, WithdrawType.AFTER)
    _ys = YearlySimulator(1000.00, _withdraw_obj, _year, 40)
    _ys.set_data(_data)
    _ys.process()

    # print(_ys.get_simulation_values())

    print("%s -> %s %s" % (_year, _year + 29, _ys.is_bankrupt()))
    # if _ys.is_bankrupt():
    #    #print("%s -> %s True" % (_year, _year+29))
    #    print(_ys.get_simulation_values())
    # else:
    #    _values=_ys.get_simulation_values()
    #    #print(_values)
    #    print("  values:", stats(list(_values.values())))
    #    #print("  withdraws:", stats(_ys.get_withdraw_values()))

    _out.writerow([_year, _year + 29] + list(_ys.get_simulation_values().values()))

del _out
# _withdraw_obj=BasicWithdrawObj(40.0, 4.0, WithdrawTimingType.AFTER)
# _withdraw_obj=GuardRailWithdrawObj(1000 * 0.04, 3.0, 5.0, 3.0)

# _ys=YearlySimulator(1000.00, _withdraw_obj, 2004, 20)
# _ys.set_data(_data)
# _ys.process()
# print(_ys.get_simulation_values())
# print(_withdraw_obj.get_withdraws())
