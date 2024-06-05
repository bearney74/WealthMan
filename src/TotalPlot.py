import matplotlib.pyplot as plt
import numpy as np

import matplotlib.collections as mcol
from matplotlib.legend_handler import HandlerLineCollection, HandlerTuple
from matplotlib.lines import Line2D

import collections

class TotalPlot:
  def __init__(self, data):
      self.years=[]
      self.dict=collections.defaultdict(list)
      
      for _de in data:
          if _de.Year not in self.years:
             self.years.append(_de.Year)
          self.dict[_de.Category].append(_de.Value)
    
  def plot(self):
      fig, ax = plt.subplots()

      _categories=[]
      _plots=[]
      for _cat, _data in self.dict.items():
          _l, = ax.plot(self.years, _data)
          _plots.append(_l)
          _categories.append(_cat)

      ax.legend(_plots, _categories, loc='upper right', shadow=True)
      ax.set_xlabel('Year')
      ax.set_ylabel('Dollars')
      ax.set_title('Totals')
      plt.show()


class CategoryPlot:
  def __init__(self, data):
      self.years=[]
      self.dict=collections.defaultdict(list)
      
      for _de in data:
          if _de.Year not in self.years:
             self.years.append(_de.Year)
          self.dict[_de.Name].append(_de.Value)
    
  def plot(self):
      fig, ax = plt.subplots()

      _categories=[]
      _plots=[]
      for _cat, _data in self.dict.items():
          _l, = ax.plot(self.years, _data)
          _plots.append(_l)
          _categories.append(_cat)

      ax.legend(_plots, _categories, loc='upper left', shadow=True)
      ax.set_xlabel('Year')
      ax.set_ylabel('Dollars')
      ax.set_title('Assets')
      plt.show()

if __name__ == '__main__':
   from Forecast import Forecast

   _f = Forecast("../tests/TestCases/JohnJaneDoe.xml")
   #_f = Forecast("../tests/TestCases/ChuckJaneSmith.xml")
   _dt=_f.execute()
   
   #_data=_dt.get_totals_data()
   _data=_dt.get_asset_data()
   #_tp=TotalPlot(_data)
   _tp=CategoryPlot(_data)
   _tp.plot()