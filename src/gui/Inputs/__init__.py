from PyQt6.QtWidgets import QTabWidget, QToolBar, QMainWindow, QComboBox
from PyQt6.QtGui import QAction, QIcon

from libs.DataVariables import DataVariables
from libs.Projections import Projections
from libs.TableData import TableData

from .BasicInfo import BasicInfoTab
from .GlobalVariables import GlobalVariablesTab
from .IncomeInfo import IncomeInfoTab
from .AssetInfo import AssetInfoTab
from .ExpenseInfo import ExpenseInfoTab


class InputsTab(QMainWindow):
    def __init__(self, parent=None):
        super(InputsTab, self).__init__(parent)

        self.parent=parent
        #self._previous_tab_name = None
        _toolbar = QToolBar("Inputs Toolbar")
        _toolbar.addAction(self.clear_forms_action())
        _toolbar.addAction(self.calculate_projection_action())
        self.addToolBar(_toolbar)

        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.onTabChange)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.BasicInfoTab = BasicInfoTab(self)
        self.IncomeInfoTab = IncomeInfoTab(self, self.BasicInfoTab)
        self.AssetInfoTab = AssetInfoTab(self, self.BasicInfoTab)
        self.ExpenseInfoTab = ExpenseInfoTab(self, self.BasicInfoTab)
        self.GlobalVariablesTab = GlobalVariablesTab(self)

        self.tabs.addTab(self.BasicInfoTab, "Basic Info")
        self.tabs.addTab(self.IncomeInfoTab, "Income")
        self.tabs.addTab(self.ExpenseInfoTab, "Expenses")
        self.tabs.addTab(self.AssetInfoTab, "Assets")
        self.tabs.addTab(self.GlobalVariablesTab, "Global Variables")

        self.setCentralWidget(self.tabs)

    def onTabChange(self, i):
        _tabName = self.tabs.tabText(i)
        match _tabName:
            case "Assets":
                self.AssetInfoTab._spouseinfo.setEnabled(
                    self.BasicInfoTab.client_is_married()
                )
            case "Income":
                self.IncomeInfoTab.spouseSS.setEnabled(
                    self.BasicInfoTab.client_is_married()
                )
                self.IncomeInfoTab.pension1OwnerLabel.setEnabled(
                    self.BasicInfoTab.client_is_married()
                )
                self.IncomeInfoTab.pension1Owner.setEnabled(
                    self.BasicInfoTab.client_is_married()
                )
                self.IncomeInfoTab.pension2OwnerLabel.setEnabled(
                    self.BasicInfoTab.client_is_married()
                )
                self.IncomeInfoTab.pension2Owner.setEnabled(
                    self.BasicInfoTab.client_is_married()
                )
                
                for _i in range(1, self.IncomeInfoTab.gridLayout.rowCount()):
                    _item = self.IncomeInfoTab.gridLayout.itemAtPosition(_i, 3)
                    # print(_item)
                    if isinstance(
                        _item.widget(), QComboBox
                    ):  # this is probably a person/owner
                        _item.widget().setEnabled(self.BasicInfoTab.client_is_married())

            case "Expenses":
                for _i in range(1, self.ExpenseInfoTab.gridLayout.rowCount()):
                    _item = self.ExpenseInfoTab.gridLayout.itemAtPosition(_i, 3)
                    # print(_item)
                    if isinstance(
                        _item.widget(), QComboBox
                    ):  # this is probably a person/owner
                        _item.widget().setEnabled(self.BasicInfoTab.client_is_married())

        # self._previous_tab_name = _tabName

    def clear_forms_action(self):
        _action = QAction("Clear forms", self)
        _action.setIcon(QIcon("resources/clear_form.png"))
        _action.setStatusTip("Clear Forms")
        _action.triggered.connect(lambda x: self.clear_forms())
        return _action

    def calculate_projection_action(self):
        _action = QAction("Projection", self)
        _action.setIcon(QIcon("resources/projections.png"))
        _action.setStatusTip("Create Data Projection")
        _action.setToolTip("Create Data Projection")
        _action.triggered.connect(lambda x: self.create_projection())
        return _action

    def clear_forms(self):
        self.BasicInfoTab.clear_form()
        self.AssetInfoTab.clear_form()
        self.IncomeInfoTab.clear_form()
        self.ExpenseInfoTab.clear_form()
        self.GlobalVariablesTab.clear_form()

    def create_projection(self):
        dv = DataVariables()

        self.BasicInfoTab.export_data(dv)
        self.IncomeInfoTab.export_data(dv)
        self.ExpenseInfoTab.export_data(dv)
        self.AssetInfoTab.export_data(dv)
        self.GlobalVariablesTab.export_data(dv)
        
        self.parent.statusbar.showMessage("Calculating projections")
        _p = Projections(dv)
        _projectionData = _p.execute()
        self.parent.AnalysisTab.projectionData = _projectionData
        self.parent.AnalysisTab.tableData = TableData(_projectionData, _p.InTodaysDollars)
        
        #self.parent.AnalysisTab.reset()
        self.parent.showAnalysisTab(True)