import collections
import matplotlib

matplotlib.use("QtAgg")

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import logging

logger = logging.getLogger(__name__)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots()
        super(MplCanvas, self).__init__(self.fig)


class MyChart(QWidget):
    def __init__(self, parent=None, width=5, height=45, dpi=100):
        super(MyChart, self).__init__(parent)
        self.title = ""

        _layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=width, height=height, dpi=dpi)
        self.canvas.axes.set_xlabel("Year")
        self.canvas.axes.set_ylabel("Dollars")
        _layout.addWidget(self.canvas)
        self.setLayout(_layout)

    def setTitle(self, title):
        self.title = title

    def setSubTitle(self, subtitle):
        self.subtitle = subtitle

    def show(self, flag: bool):
        assert isinstance(flag, bool)

        if flag:
            self.canvas.show()
        else:
            self.canvas.hide()

    def stackplot(self, years, values, labels, legend_location="upper left"):
        self.canvas.axes.clear()

        try:
            _output = self.canvas.axes.stackplot(
                years, values, labels=labels, alpha=0.8
            )
        except ValueError as e:
            logger.error(
                "Please enter data into income/asset tabs to generate custom charts"
            )
            logger.error("%s" % e)
            logger.error(
                "plot arugments: years=%s, values=%s, labels=%s"
                % (years, values, labels)
            )
            self.canvas.fig.text(
                0.5,
                0.9,
                "",
                horizontalalignment="center",
            )
            self.canvas.fig.draw(self.canvas.fig.canvas.renderer)
            return

        self.canvas.fig.suptitle(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")
        self.canvas.axes.legend(loc=legend_location)

        def format_string(x, pos):
            return "${:,d}".format(int(x))

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))
        for _line in _output:
            if _line.figure is not None:
                _line.figure.canvas.draw()

    def plotlines(self, years, data, labels, legend_location="upper left"):
        self.canvas.axes.clear()

        self.canvas.fig.suptitle(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")

        def format_string(x, pos):
            return "${:,d}".format(int(x))

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))

        # _num=len(labels)
        for _label in labels:
            _out = self.canvas.axes.plot(years, data[_label], label=_label)
            for _line in _out:
                if _line.figure is not None:
                    _line.figure.canvas.draw()

        self.canvas.axes.legend(loc=legend_location)
        # for some reason the legend does not get update unless we call the draw below...
        self.canvas.fig.draw(self.canvas.fig.canvas.renderer)

        # self.show(True)


class CustomChartTab(QWidget):
    def __init__(self, parent=None):
        super(CustomChartTab, self).__init__(parent)
        self.parent = parent

        self.variables = QComboBox(self.parent)
        self.variables.addItems(
            [
                "Asset Totals",
                "Asset Contribution Totals",
                "Income Totals",
                "Income VS Expense",
            ]
        )

        self.chart = MyChart(self, width=5, height=45, dpi=100)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.variables)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addWidget(self.chart)
        self.setLayout(layout)

        self.variables.currentIndexChanged.connect(self._selectionchange)

    def _selectionchange(self, i):
        if self.parent.projectionData is None:
            return

        match self.variables.currentText():
            case "Asset Totals":
                self.AssetTotals()
            case "Asset Contribution Totals":
                self.AssetContributionTotals()
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

        self.chart.setTitle("Asset Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")
        else:
            self.chart.setSubTitle("")

        self.chart.stackplot(_years, _data.values(), _data.keys())
        self.chart.show(True)

    def IncomeTotals(self):
        _years = []

        _data = collections.defaultdict(list)
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear.data not in _years:
                    _years.append(_record.projectionYear.data)

                for _dataItem in _record.incomeSources:
                    _data[_dataItem.header].append(_dataItem.data)

        self.chart.setTitle("Income Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")
        else:
            self.chart.setSubTitle("")

        self.chart.stackplot(
            _years, _data.values(), _data.keys(), legend_location="upper right"
        )
        self.chart.show(True)

    def AssetContributionTotals(self):
        _years = []

        _data = collections.defaultdict(list)
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear.data not in _years:
                    _years.append(_record.projectionYear.data)

                for _dataItem in _record.assetContributions:
                    _data[_dataItem.header].append(_dataItem.data)

        self.chart.setTitle("Asset Contribution Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")
        else:
            self.chart.setSubTitle("")

        if len(_data.values()) > 0:
            self.chart.stackplot(
                _years, _data.values(), _data.keys(), legend_location="upper right"
            )
            self.chart.show(True)
        else:
            #self.chart.stackplot([], [], [])
            #self.chart.canvas.axes.clear()
            self.chart.show(False)

    
    def IncomeVsExpenses(self):
        _years = []

        _data = collections.defaultdict(list)
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear.data not in _years:
                    _years.append(_record.projectionYear.data)

                _data["Income"].append(_record.incomeTotal.data)
                _data["Expense"].append(_record.expenseTotal.data)

    
        self.chart.setTitle("Income Vs Expenses")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")
        else:
            self.chart.setSubTitle("")

        if len(_data.values()) > 0:
            self.chart.plotlines(
                _years, _data, _data.keys(), legend_location="upper right"
            )
        else:
            self.chart.plotlines([], [], [])
        self.chart.show(True)
