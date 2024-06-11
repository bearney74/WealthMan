from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout, QComboBox

import sys
sys.path.append("guihelpers")
from Entry import AgeEntry, FloatEntry

class GlobalVariablesTab(QWidget):
  def __init__(self, parent=None):
      super(GlobalVariablesTab, self).__init__(parent)

      formlayout=QFormLayout()

      self._forecast_years=AgeEntry()   #2 digit integer
      formlayout.addRow(QLabel("Years to Forecast:"), self._forecast_years)
      
      self._Inflation=FloatEntry(min=-10.0, max=10.0, num_decimal_places=1)
      formlayout.addRow(QLabel("Inflation:"), self._Inflation)

      self._SS_Cola=FloatEntry(min=0, max=10.0, num_decimal_places=1)
      formlayout.addRow(QLabel("Social Security Cola:"), self._SS_Cola)
                             
      self._WithdrawOrder=QComboBox()
      self._WithdrawOrder.setFixedWidth(200)
      self._WithdrawOrder.addItems(["TaxDeferred,Regular,TaxFree",
                                   "Regular,TaxFree,TaxDeferred",
                                   "TaxFree, TaxDeferred,Regular",
                                   "Regular,TaxDeferred,TaxFree",
                                   "TaxDeferred,TaxFree,Regular",
                                   "Regular,TaxDeferred,TaxFree"])
      formlayout.addRow(QLabel("Withdrawal Order"), self._WithdrawOrder)
      
      self.setLayout(formlayout)
