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


class StackChart(QWidget):
    def __init__(self, parent=None, width=5, height=45, dpi=100):
        super(StackChart, self).__init__(parent)
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

    def plot(self, years, values, labels, legend_location="upper left"):
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
                "Please enter data into income/asset tabs to generate custom charts",
                horizontalalignment="center",
            )
            self.canvas.fig.draw(self.canvas.fig.canvas.renderer)
            return

        self.canvas.fig.suptitle(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")
        self.canvas.axes.legend(loc=legend_location)

        def format_string(x, pos):
            _str = ""
            x = int(x)
            return f"${x:,d}"

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))
        for _line in _output:
            if _line.figure is not None:
                _line.figure.canvas.draw()


class CustomChartTab(QWidget):
    def __init__(self, parent=None):
        super(CustomChartTab, self).__init__(parent)
        self.parent = parent

        self.variables = QComboBox(self.parent)
        self.variables.addItems(
            ["Asset Totals", "Asset Contribution Totals", "Income Totals"]
        )

        self.chart = StackChart(self, width=5, height=45, dpi=100)

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
                if _record.projectionYear not in _years:
                    _years.append(_record.projectionYear)

                for _name, _value in _record.assetSources.items():
                    _data[_name].append(_value)

                if _record.surplusBalance > 0:
                    _surplus_flag = True
                _data["Surplus"].append(_record.surplusBalance)

        if (
            not _surplus_flag
        ):  # we have no surplus data, so lets delete that from the legend..
            del _data["Surplus"]

        self.chart.setTitle("Asset Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")

        self.chart.plot(_years, _data.values(), _data.keys())
        self.chart.show(True)

    def IncomeTotals(self):
        _years = []

        _data = collections.defaultdict(list)
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear not in _years:
                    _years.append(_record.projectionYear)

                for _name, _value in _record.incomeSources.items():
                    _data[_name].append(_value)

        self.chart.setTitle("Income Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")

        self.chart.plot(
            _years, _data.values(), _data.keys(), legend_location="upper right"
        )
        self.chart.show(True)

    def AssetContributionTotals(self):
        _years = []

        _data = collections.defaultdict(list)
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear not in _years:
                    _years.append(_record.projectionYear)

                for _name, _value in _record.assetContributions.items():
                    _data[_name].append(_value)

        self.chart.setTitle("Asset Contribution Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")

        self.chart.plot(
            _years, _data.values(), _data.keys(), legend_location="upper right"
        )
        self.chart.show(True)
