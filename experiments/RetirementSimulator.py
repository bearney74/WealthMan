import csv


class HistoricalData:
    def __init__(self):
        self._data = {}

        with open("history.csv", "r") as _fp:
            _csv = csv.reader(_fp)

            next(_csv)  # skip header
            for _year, sp500 in _csv:
                self._data[int(_year)] = 1.0 + float(sp500) / 100.0

        assert len(self._data) > 1

        self._data = dict(sorted(self._data.items()))

    def get_data(self, begin_year, end_year):
        _list = []

        for _year, _return in self._data.items():
            if _year >= begin_year and _year <= end_year:
                _list.append((_year, _return))

        return _list


class RetirementSimulator:
    def __init__(self, begin_year, end_year, balance, incomes, expenses):
        self.balance = balance

        self.incomes = incomes
        self.expenses = expenses

        _hd = HistoricalData()
        self._data = _hd.get_data(begin_year, end_year)

    def execute(self):
        _success = True
        for _year, _return in self._data:
            if _year in self.incomes:
                self.balance += self.incomes[_year]

            if _year in self.expenses:
                self.balance -= self.expenses[_year]

            # print(self.balance, _return)
            self.balance *= _return

            if self.balance <= 0:
                _success = False

        return _success, int(self.balance)


if __name__ == "__main__":

    def single_run(begin_year, end_year):
        balance = 100
        incomes = {}
        expenses = {}

        for _i in range(begin_year, end_year + 1):
            expenses[_i] = 5

        _rs = RetirementSimulator(begin_year, end_year, balance, incomes, expenses)
        print("%s->%s: %s, %s" % tuple((begin_year, end_year) + _rs.execute()))

    # single_run(2000, 2010)
    # single_run(2001, 2011)
    for _begin_year in range(1926, 2023 - 30 + 1):
        single_run(_begin_year, _begin_year + 30)
