from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QToolBar
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QAction

from .BasicInfo import BasicInfoTab
from .GlobalVariables import GlobalVariablesTab
from .IncomeInfo import IncomeSourceTab
from .AssetInfo import AssetInfoTab

class InputsTab(QMainWindow):
  def __init__(self, parent=None):
      super(InputsTab, self).__init__(parent)
      
      _toolbar=QToolBar("Inputs Toolbar")
      _toolbar.addAction(self.clear_forms_action())
      self.addToolBar(_toolbar)
      
      self.tabs = QTabWidget()
      self.tabs.setTabPosition(QTabWidget.TabPosition.South)
      
      #Expense_tab = ttk.Frame(tabControl)
      self.BasicInfoTab=BasicInfoTab()
      self.IncomeSourceTab=IncomeSourceTab(parent=parent)
      self.AssetTab=AssetInfoTab(self.BasicInfoTab)
      self.GlobalVariablesTab = GlobalVariablesTab()

      self.tabs.addTab(self.BasicInfoTab, "Basic Info")
      self.tabs.addTab(self.IncomeSourceTab, "Income")
      self.tabs.addTab(QWidget(), "Expenses")
      self.tabs.addTab(self.AssetTab, "Assets")
      self.tabs.addTab(self.GlobalVariablesTab, "Global Variables")
      
      #mainLayout = QVBoxLayout()
      #mainLayout.addWidget(self.tabs)
      #self.setLayout(mainLayout)
      self.setCentralWidget(self.tabs)
      
  def clear_forms_action(self):
      _action=QAction("Clear forms", self)
      _action.setStatusTip("Clear Forms")
      _action.triggered.connect(lambda x: self.clear_forms())
      return _action
      
  def clear_forms(self):
      self.BasicInfoTab.clear_form()