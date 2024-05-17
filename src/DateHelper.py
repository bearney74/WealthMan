from datetime import date


class DateHelper:
  """ calculates the number of days between 2 dates in the same year"""

  def __init__(self, begin_dt:date, end_dt:date):
      self._begin_date=begin_dt
      self._end_date=end_dt
      
      #this class should only be used for a single year  (ie where begin_date and end_date occur in the same year)
      if self._begin_date is not None and self._end_date is not None:
          print(self._begin_date.year, self._end_date.year)
          assert(self._begin_date.year == self._end_date.year)
      
  def days_in_year(self) -> float:
      if self._end_date is None and self._begin_date is None:
          return 365.0
        
      if self._end_date is None:
         _end_of_year=date(self._begin_date.year, 12, 31)
         _diff = _end_of_year - self._begin_date
         return _diff.days + 1
          
      if self._begin_date is None:
         _beginning_of_year=date(self._end_date.year, 1, 1)
         _diff = self._end_date - _beginning_of_year
         return _diff.days + 1
          
      _diff = self._end_date - self._begin_date
      return _diff.days + 1
    
  def percent_of_year(self) -> float:
      if self._end_date is None and self._begin_date is None:
          return 100.0
      
      return 100.0 * self.days_in_year()/365.0