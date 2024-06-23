from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from libs.DataVariables import DataVariables
from .DataTable import DataTableTab


class AnalysisTab(QWidget):
    def __init__(self, parent=None):
        super(AnalysisTab, self).__init__(parent)

        self.parent = parent
        self.tabs = QTabWidget()

        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.DataTableTab = DataTableTab(self)

        self.tabs.currentChanged.connect(self.onTabChange)
        self.tabs.addTab(QWidget(), "Dashboard")
        self.tabs.addTab(self.DataTableTab, "Details")
        self.tabs.addTab(QWidget(), "Charts")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def onTabChange(self, i):
        _tabName = self.tabs.tabText(i)
        # print(_tabName)
        if _tabName == "Details":
            # self.DataTableTab.table.setEnabled(False)
            # self.DataTableTab.waiting.show()
            dv = DataVariables()

            # print("exporting data..")
            self.parent.InputsTab.BasicInfoTab.export_data(dv)
            self.parent.InputsTab.IncomeInfoTab.export_data(dv)
            self.parent.InputsTab.ExpenseInfoTab.export_data(dv)
            self.parent.InputsTab.AssetInfoTab.export_data(dv)
            self.parent.InputsTab.GlobalVariablesTab.export_data(dv)
            # print("creating table")
            self.DataTableTab.createTable(dv)
            # print("done creating table")
            # self.DataTableTab.waiting.hide()
            # self.DataTableTab.table.setEnabled(True)

        self._previous_tab_name = _tabName
