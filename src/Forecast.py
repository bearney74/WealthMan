# look at persons and see
import sys

sys.path.append("xml/Import")
from Import import Import

# from EnumTypes import AccountType


class Forecast:
  def __init__(self, xml_file, current_year: int = 2024):
      _i = Import(xml_file)
      self._vars = _i.get_data()
      self._current_year = current_year

  def execute(self):
      _person1 = self._vars["Persons"]["1"]
      _person2 = self._vars["Persons"]["2"]
      for _i in range(self._vars["GlobalVars"].YearsToForecast):
          _year = self._current_year + _i
          # figure out the total income for the next year
          print(
                _year,
                _person1.calc_age_by_year(_year),
                _person2.calc_age_by_year(_year),
                " ",
                end=" ",
          )

          _income_total = 0
          for _src in self._vars["IncomeSources"]:
              _income = _src.calc_balance_by_year(_year)
              # print(_year, _src.Name, _income)
              print(_income, end=" ")
              _income_total += _income  # _src.calc_income_by_year(_year)
          print(_income_total, end=" *** ")

          # print("\n")
          # output expenses..
          _expense_total = 0
          for _src in self._vars["Expenses"]:
              _expense = _src.calc_balance_by_year(_year)
              print(_expense, end=" ")

              _expense_total += _expense
          print(_expense_total, end=" *** ")

          print(_income_total - _expense_total, end= " *** ")

          _total=0
          for _src in self._vars["Assets"]:
              _balance = _src.calc_balance_by_year(_year)
              _total+=_balance
              print(_balance, end=" ")
          print(_total)


if __name__ == "__main__":
   _f = Forecast("../tests/TestCases/JohnJaneDoe.xml")
   _f.execute()
