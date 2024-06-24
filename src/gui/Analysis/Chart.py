#import sys
import matplotlib
matplotlib.use('QtAgg')

from PyQt6.QtWidgets import QWidget,QVBoxLayout, QHBoxLayout, QComboBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, StrMethodFormatter

from libs.TableData import TableData

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)
        fig, self.axes=plt.subplots()
        super(MplCanvas, self).__init__(fig)

class Chart(QWidget):
  def __init__(self, parent=None, width=5, height=45, dpi=100):
      super(Chart, self).__init__(parent)
      self.title=""

      _layout=QVBoxLayout()
      self.canvas=MplCanvas(self, width=width, height=height, dpi=dpi)
      #print(dir(self.canvas.axes))
      self.canvas.axes.set_xlabel("Year")
      self.canvas.axes.set_ylabel("Dollars")
      _layout.addWidget(self.canvas)
      self.setLayout(_layout)

  def setTitle(self, title):
      self.title=title

  def show(self, flag: bool):
      assert isinstance(flag, bool)
      
      if flag:
          self.canvas.show()
      else:
          self.canvas.hide()

  def plot(self, data):
      _x_data=[]
      _y_data=[]
      #print(data)
      for _x, _y in data:
          _x_data.append(_x)
          _y_data.append(_y)
            
      self.canvas.axes.clear()
      self.canvas.axes.set_title(self.title)
      _line,=self.canvas.axes.plot(_x_data, _y_data)
      #self.canvas.axes.yaxis.set_major_formatter('${x:,d}')
      
      def format_string(x, pos):
          _str=""
          x=int(x)
          return f'${x:,d}'
       
      self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))
      
      self.canvas.axes.fill_between(_x_data, 0, _y_data, alpha=0.7)
      _line.figure.canvas.draw()

class ChartTab(QWidget):
  def __init__(self, parent=None):
      super(ChartTab, self).__init__(parent)
      self.parent=parent
      self.Data=[]
      
      self.variables=QComboBox(self.parent)
            
      self.chart = Chart(self, width=5, height=45, dpi=100)
      #self.chart.show(False)
      
      layout=QVBoxLayout()
      hlayout=QHBoxLayout()
      hlayout.addWidget(self.variables)
      hlayout.addStretch()
      layout.addLayout(hlayout)
      layout.addWidget(self.chart)
      self.setLayout(layout)
  
      self.variables.currentIndexChanged.connect(self._selectionchange)
      
  def setCategories(self, td:TableData):
      assert isinstance(td, TableData)
      self.variables.clear()
      #self.variables.addItems(dt.getCategories())
      self.variables.addItems(td.getFields())
      self.Data=td.Data
      
  def _selectionchange(self, i):
      #print("selection change")
      _field=self.variables.currentText()
      
      _data=[]
      for _record in self.Data:
          #print(_record.Category, _category)
          _f="%s %s" % (_record.Category, _record.Name)
          if _f == _field:
             _data.append((_record.Year, _record.Value)) 
      
      self.chart.setTitle(_field)
      self.chart.plot(_data)
      self.chart.show(True)
  
  
  