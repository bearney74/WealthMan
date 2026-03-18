import collections

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QStackedWidget

from .Charts import StackChart, MultiLineChart
import logging

logger = logging.getLogger(__name__)


class CustomChartTab(QWidget):
    def __init__(self, parent=None):
        super(CustomChartTab, self).__init__(parent)
        self.parent = parent

        self.variables = QComboBox(self.parent)
        self.variables.addItems(
            [
                "Asset Totals",
                #   "Asset Contribution Totals",
                "Income Totals",
                "Income VS Expense",
            ]
        )

        # need to use a StackedWidget to switch between a StackChart and a MultipleLinesChart
        # we use stackedWidget.setCurrentIndex(0 or 1) to switch between the charts.
        self.stackedWidget = QStackedWidget(self)

        self.stackchart = StackChart(self.stackedWidget)
        self.stackedWidget.addWidget(self.stackchart)

        self.multiplelineschart = MultiLineChart(self.stackedWidget)
        self.stackedWidget.addWidget(self.multiplelineschart)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.variables)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

        self.variables.currentIndexChanged.connect(self._selectionchange)

    def _selectionchange(self, i):
        if self.parent.projectionData is None:
            return

        match self.variables.currentText():
            case "Asset Totals":
                self.AssetTotals()
            # case "Asset Contribution Totals":
            #    self.AssetContributionTotals()
            case "Income Totals":
                self.IncomeTotals()
            case "Income VS Expense":
                self.IncomeVsExpenses()
            case _:
                logger.error(
                    "invalid custom chart '%s' " % self.variables.currentText()
                )

    def AssetTotals(self):
        _years = []
        _data = collections.defaultdict(list)

        _surplus_flag = False
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear.data not in _years:
                    _years.append(_record.projectionYear.data)

                for _dataItem in _record.assetSources:
                    _data[_dataItem.header].append(_dataItem.data)

                if _record.surplusBalance.data > 0:
                    _surplus_flag = True
                _data["Surplus"].append(_record.surplusBalance.data)

        if (
            not _surplus_flag
        ):  # we have no surplus data, so lets delete that from the legend..
            del _data["Surplus"]

        # take the values in the dict and create a list of lists..
        _list = []
        _names = list(_data.keys())
        for _name in _names:
            _list.append(_data[_name])

        self.stackedWidget.setCurrentIndex(0)  # set to stacked chart
        self.stackchart.setTitle("Asset Totals")
        self.stackchart.setXLabel("Year")
        self.stackchart.setYLabel("Dollars", units="$")
        self.stackchart.addLegend()
        if self.parent.tableData.InTodaysDollars:
            self.stackchart.setSubTitle("In Today's Dollars")
        else:
            self.stackchart.setSubTitle("")

        self.stackchart.plot_data(_years, _list, _names)
        self.stackchart.show(True)

    def IncomeTotals(self):
        self._StackChartHelper("incomeSources", "Income Totals")

    # def AssetContributionTotals(self):
    #    self._StackChartHelper("assetTotalContributions", "Asset Contribution Totals")

    def _StackChartHelper(self, attr, title):
        _years = []

        _dict = collections.defaultdict(list)
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear.data not in _years:
                    _years.append(_record.projectionYear.data)

                for _dataItem in getattr(_record, attr):
                    _dict[_dataItem.header].append(_dataItem.data)

        _data = []
        _names = list(_dict.keys())
        for _name in _names:
            _data.append(_dict[_name])

        self.stackedWidget.setCurrentIndex(0)  # set to stacked chart

        self.stackchart.setTitle(title)
        self.stackchart.setXLabel("Year")
        self.stackchart.setYLabel("Dollars", units="$")
        self.stackchart.addLegend()
        if self.parent.tableData.InTodaysDollars:
            self.stackchart.setSubTitle("In Today's Dollars")
        else:
            self.stackchart.setSubTitle("")

        if len(_names) > 0:
            self.stackchart.plot_data(_years, _data, _names)
            self.stackchart.show(True)
        else:
            self.stackchart.show(False)

    def IncomeVsExpenses(self):
        _years = []

        _incomes = []
        _expenses = []
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear.data not in _years:
                    _years.append(_record.projectionYear.data)

                _incomes.append(_record.incomeTotal.data)
                _expenses.append(_record.expenseTotal.data)

        self.stackedWidget.setCurrentIndex(1)  # set to multiple lines chart

        self.multiplelineschart.setTitle("Income Vs Expenses")
        self.multiplelineschart.setXLabel("Year")
        self.multiplelineschart.setYLabel("Dollars", units="$")
        self.multiplelineschart.addLegend()
        if self.parent.tableData.InTodaysDollars:
            self.multiplelineschart.setSubTitle("In Today's Dollars")
        else:
            self.multiplelineschart.setSubTitle("")

        if len(_incomes) > 0:
            self.multiplelineschart.plot_data(
                _years, [_incomes, _expenses], ["Incomes", "Expenses"]
            )
        else:
            self.multiplelineschart.plot_data([], [], [])
        self.multiplelineschart.show(True)
