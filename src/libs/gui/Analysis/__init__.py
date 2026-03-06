from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from .DataTable import (
    DataTableTab,
    IncomeDataTableTab,
    ExpenseDataTableTab,
    AssetDataTableTab,
    TaxDataTableTab,
)
from .Chart import ChartTab
from .CustomChart import CustomChartTab

from .MonteCarloSimulation import MonteCarloTab
from .HistoricalAnalysis import HistoricalAnalysisTab


class AnalysisTab(QWidget):
    def __init__(self, parent):
        super(AnalysisTab, self).__init__(parent)

        self.parent = parent
        # projectionData is generated when a user clicks on the Analysis tab
        self.projectionData = None
        self.tableData = None

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.IncomeDataTableTab = IncomeDataTableTab(self)
        self.ExpenseDataTableTab = ExpenseDataTableTab(self)
        # Assets
        self.AssetDataTableTab = AssetDataTableTab(self)

        # Taxes
        self.TaxDataTableTab = TaxDataTableTab(self)

        self.DataTableTab = DataTableTab(self)
        self.ChartTab = ChartTab(self)
        self.CustomChartTab = CustomChartTab(self)

        # advanced tabs
        self.MonteCarloTab = MonteCarloTab(self)
        self.HistoricalAnalysisTab = HistoricalAnalysisTab(self)

        self.tabs.currentChanged.connect(self.onTabChange)

        self.tabs.addTab(self.IncomeDataTableTab, "Income Details")
        self.tabs.addTab(self.ExpenseDataTableTab, "Expense Details")
        self.tabs.addTab(self.AssetDataTableTab, "Asset Details")
        self.tabs.addTab(self.TaxDataTableTab, "Tax Details")
        self.tabs.addTab(self.DataTableTab, "Details")
        self.tabs.addTab(self.ChartTab, "Charts")
        self.tabs.addTab(self.CustomChartTab, "Custom Charts")
        self.tabs.addTab(self.MonteCarloTab, "Monte Carlo")
        self.tabs.addTab(self.HistoricalAnalysisTab, "Historical")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    def reset(self):
        self.parent.statusbar.showMessage("updating Analysis GUI")

        self.IncomeDataTableTab.createTable()
        self.ExpenseDataTableTab.createTable()
        self.AssetDataTableTab.createTable()
        self.TaxDataTableTab.createTable()
        self.DataTableTab.createTable()
        self.ChartTab.setCategories()

        self.parent.statusbar.showMessage("Done updating Analysis GUI", 2000)

    def onTabChange(self, i):
        _tabName = self.tabs.tabText(i)

        match _tabName:
            case "Custom Charts":
                self.CustomChartTab.AssetTotals()
            # case "Monte Carlo":
            #    self.MonteCarloTab.CalcInputs()
