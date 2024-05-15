from datetime import date

class DateHelper:
  def __init__(self, begin_dt:str, end_dt:str, death_dates=list(date)):
      self._death_dates=death_dates
      
  def _helper(self, dt: str) -> date:
      if dt is None or dt is 'None':
         return None
    
      
  def after_death(self, dt:date) -> list(str):
      """ returns a list of persons that are dead after the dt date """
      
      _death_persons=[]
      for _person_num, _death_date in self._death_dates:
          if dt.year > _death_date.year:   # this is after the death year..
             _death_persons.append(_person_num)
          elif dt.year == _death_date.year:
             if dt.month > _death_date.month:
                _death_persons.append(_person_num)
             elif dt.month == _death_date.month:
                 if dt.day >= _death_date.day:
                     _death_persons.append(_person_num)
                     
      return _death_persons