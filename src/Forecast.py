
# look at persons and see
import sys
sys.path.append("xml/Import")
from Import import Import

class Forecast:
  def __init__(self, xml_file, current_year=2024):
      _i=Import(xml_file)
      self._vars=_i.get_data()
      self._current_year=2024


  def execute(self):
      _person1=self._vars['Persons']['1']
      _person2=self._vars['Persons']['2']
      for _i in range(self._vars['GlobalVars'].YearsToForecast):
          _year = self._current_year + _i
          #figure out the total income for the next year
          _total=0
          for _src in self._vars['IncomeSources']:
              _total+=_src.calc_income_by_year(_year)
          print(_year, _person1.calc_age_by_year(_year), _person2.calc_age_by_year(_year), _total)


if __name__ == '__main__':
    _f=Forecast("../TestCases/JohnJaneDoe.xml")
    _f.execute()