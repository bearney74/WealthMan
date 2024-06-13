from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from gui.BasicInfo import BasicInfoTab
from gui.GlobalVariables import GlobalVariablesTab
#from IncomeInfo import IncomeInfoFrame
#from AssetInfo import AssetInfoFrame


class Inputs(QWidget):
  def __init__(self, parent=None):
      super(Inputs, self).__init__(parent)
      
      self.tabs = QTabWidget()
      self.tabs.setTabPosition(QTabWidget.TabPosition.South)
      
      #self.Basic_tab = BasicInfoFrame(tabControl)
      #self.Income_tab = IncomeInfoFrame(tabControl)
      #Expense_tab = ttk.Frame(tabControl)
      ##self.Asset_tab = AssetInfoFrame(tabControl, self.Basic_tab)
      self.BasicInfoTab=BasicInfoTab()
      self.GlobalVariablesTab = GlobalVariablesTab()

      self.tabs.addTab(self.BasicInfoTab, "Basic Info")
      self.tabs.addTab(QWidget(), "Income")
      self.tabs.addTab(QWidget(), "Expenses")
      self.tabs.addTab(QWidget(), "Assets")
      self.tabs.addTab(self.GlobalVariablesTab, "Global Variables")
      
      mainLayout = QVBoxLayout()
      mainLayout.addWidget(self.tabs)
      self.setLayout(mainLayout)