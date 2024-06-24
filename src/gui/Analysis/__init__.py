from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from .DataTable import DataTableTab
from .Chart import ChartTab
from .CustomChart import CustomChartTab

class AnalysisTab(QWidget):
    def __init__(self, parent=None):
        super(AnalysisTab, self).__init__(parent)

        self.parent = parent
        self.tabs = QTabWidget()

        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.DataTableTab = DataTableTab(self)
        self.ChartTab = ChartTab(self)
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
        #print(_tabName)
        match _tabName:
          case "Details":
              self.DataTableTab.createTable(self.parent.tableData)
          case "Charts":
              self.ChartTab.setCategories(self.parent.tableData)
              self.ChartTab.chart.show(False)
          case "Custom Charts":
              self.CustomChartTab.populate(self.parent.tableData)
        