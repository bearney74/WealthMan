
import logging

logger = logging.getLogger(__name__)

# since the single and married jointly values don't change with inflation, how do I work with these values
# when looking at "todays dollars"?   I know I can pass a variable in to do this calc..
#for example if "inflation" is 3.0, we could assume 0.97 for each year of decrease for each value.
# for n years this would be 0.97^n
class ProvisionalIncome:
  def __init__(self, filing_status, mult=1.0):
      self._filing_status=filing_status
      
      self._single={'0': {'Begin': 0, 'End': 24999 * mult},
                    '50': {'Begin': 25000 * mult, 'End': 34000 * mult},
                    '85': {'Begin': 34001 * mult, 'End': 999_999_999_999}}
      
      self._single=dict(sorted(self._single.items()))
      
      self._married_jointly={'0': {'Begin': 0, 'End': 31999 * mult},
                             '50': {'Begin': 32000 * mult, 'End': 44000 * mult},
                             '85': {'Begin': 44001 * mult, 'End': 999_999_999_999}}
      self._married_jointly=dict(sorted(self._married_jointly.items()))
                             
  def calc_ss_taxable(self, provisional_income, ss_income):
      return int(self.get_rate(provisional_income, ss_income)/100.0 * ss_income)
      
  def get_rate(self, provisional_income:int, ss_income:int) -> int:
      _income = provisional_income + 0.5 * ss_income
      #print(_income)
      if self._filing_status == 'Single':
          for _rate, _dict in self._single.items():
              _begin=_dict['Begin']
              _end=_dict['End']
              
              if _income >= _begin and _income <= _end:
                  return int(_rate)
      else: # self._filing_status == 'Married':
          for _rate, _dict in self._married_jointly.items():
              _begin=_dict['Begin']
              _end=_dict['End']
              
              #print(_income, _begin, _end)
              if _income >= _begin and _income <= _end:
                  return int(_rate)
      
      logger.error("We shouldn't get here...")