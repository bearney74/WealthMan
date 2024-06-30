from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from .DataTable import DataTableTab
from .Chart import ChartTab
from .CustomChart import CustomChartTab

from libs.TableData import TableData


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
        self.ChartTab = ChartTab(self, self)
        self.CustomChartTab = CustomChartTab(self)

        self.tabs.currentChanged.connect(self.onTabChange)
        self.tabs.addTab(QWidget(), "Dashboard")
        self.tabs.addTab(self.DataTableTab, "Details")
        self.tabs.addTab(self.ChartTab, "Charts")
        self.tabs.addTab(self.CustomChartTab, "Custom Charts")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def onTabChange(self, i):
        _tabName = self.tabs.tabText(i)
        if self.projectionData is None:
            self.projectionData = self.parent.projectionData
            if self.projectionData is not None:
                self.tableData = TableData(self.parent.projectionData)
        # if self.tableData is None:
        #   self.tableData=TableData(self.parent.projectionData)

        #print(_tabName)
        match _tabName:
            case "Details":
                # _tableData=TableData(self.parent.projectionData)
                self.DataTableTab.createTable()
            case "Charts":
                self.ChartTab.setCategories()
                self.ChartTab.chart.show(False)
            case "Custom Charts":
                self.CustomChartTab.setCategories()
                #self.CustomChartTab.AssetTotals()
