from PyQt6.QtWidgets import QTabWidget, QToolBar, QMainWindow
from PyQt6.QtGui import QAction

from .BasicInfo import BasicInfoTab
from .GlobalVariables import GlobalVariablesTab
from .IncomeInfo import IncomeSourceTab
from .AssetInfo import AssetInfoTab
from .ExpenseInfo import ExpenseInfoTab


class InputsTab(QMainWindow):
    def __init__(self, parent=None):
        super(InputsTab, self).__init__(parent)

        self._previous_tab_name=None
        _toolbar = QToolBar("Inputs Toolbar")
        _toolbar.addAction(self.clear_forms_action())
        self.addToolBar(_toolbar)

        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.onTabChange)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        # Expense_tab = ttk.Frame(tabControl)
        self.BasicInfoTab = BasicInfoTab(self)
        self.IncomeSourceTab = IncomeSourceTab(self, self.BasicInfoTab)
        self.AssetTab = AssetInfoTab(self, self.BasicInfoTab)
        self.ExpenseTab = ExpenseInfoTab(self, self.BasicInfoTab)
        self.GlobalVariablesTab = GlobalVariablesTab(self)

        self.tabs.addTab(self.BasicInfoTab, "Basic Info")
        self.tabs.addTab(self.IncomeSourceTab, "Income")
        self.tabs.addTab(self.ExpenseTab, "Expenses")
        self.tabs.addTab(self.AssetTab, "Assets")
        self.tabs.addTab(self.GlobalVariablesTab, "Global Variables")

        # mainLayout = QVBoxLayout()
        # mainLayout.addWidget(self.tabs)
        # self.setLayout(mainLayout)
        self.setCentralWidget(self.tabs)

    def onTabChange(self, i):
        if self._previous_tab_name is not None:
           if self._previous_tab_name == "Basic Info":
              if not self.BasicInfoTab.validate_form():
                 return

        _tabName=self.tabs.tabText(i)
        if _tabName == "Assets":
            self.AssetTab._spouseinfo.setEnabled(self.BasicInfoTab.client_is_married())
        
        self._previous_tab_name=_tabName
        #print(i)

    def clear_forms_action(self):
        _action = QAction("Clear forms", self)
        _action.setStatusTip("Clear Forms")
        _action.triggered.connect(lambda x: self.clear_forms())
        return _action

    def clear_forms(self):
        self.BasicInfoTab.clear_form()
        self.AssetTab.clear_form()
        self.IncomeSourceTab.clear_form()
        self.ExpenseTab.clear_form()
        self.GlobalVariablesTab.clear_form()
