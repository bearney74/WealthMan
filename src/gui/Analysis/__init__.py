from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from .DataTable import DataTableTab
from .Chart import ChartTab
from .CustomChart import CustomChartTab


class AnalysisTab(QWidget):
    def __init__(self, parent):
        super(AnalysisTab, self).__init__(parent)

        self.parent = parent
        # projectionData is generated when a user clicks on the Analysis tab
        self.projectionData = None
        self.tableData = None

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.DataTableTab = DataTableTab(self)
        self.ChartTab = ChartTab(self)
        self.CustomChartTab = CustomChartTab(self)

        # self.tabs.currentChanged.connect(self.onTabChange)
        # self.tabs.addTab(QWidget(), "Dashboard")
        self.tabs.addTab(self.DataTableTab, "Details")
        self.tabs.addTab(self.ChartTab, "Charts")
        self.tabs.addTab(self.CustomChartTab, "Custom Charts")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def reset(self):
        self.parent.statusbar.showMessage("updating Analysis GUI")
        self.DataTableTab.createTable()
        self.ChartTab.setCategories()
        # self.CustomChartTab.AssetTotals()
        self.parent.statusbar.showMessage("Done updating Analysis GUI", 2000)
