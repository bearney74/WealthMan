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
        # print(dir(self.canvas.axes))
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

        # print(_output)

        self.canvas.fig.suptitle(self.title)
        # self.canvas.axes.set_title(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")
        self.canvas.axes.legend(loc=legend_location)

        # self.canvas.axes.clear()

        def format_string(x, pos):
            _str = ""
            x = int(x)
            return f"${x:,d}"

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))
        # self.canvas.axes.fill_between(values, 0, years, alpha=0.7)
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
        # self.chart.show(False)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.variables)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addWidget(self.chart)
        self.setLayout(layout)

        self.variables.currentIndexChanged.connect(self._selectionchange)

    def _selectionchange(self, i):
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

        _data = {}
        _data["Client IRA"] = []
        _data["Client Roth IRA"] = []
        _data["Spouse IRA"] = []
        _data["Spouse Roth IRA"] = []
        _data["Regular"] = []
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear not in _years:
                    _years.append(_record.projectionYear)

                for _name, _value in _record.assetSources.items():
                    _data[_name].append(_value)

        # self.chart.show(False)
        self.chart.setTitle("Asset Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")

        self.chart.plot(_years, _data.values(), _data.keys())
        self.chart.show(True)

    def IncomeTotals(self):
        _years = []

        _data = {}
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear not in _years:
                    _years.append(_record.projectionYear)

                for _name, _value in _record.incomeSources.items():
                    if _name not in _data:
                        _data[_name] = []
                    _data[_name].append(_value)

        # self.chart.show(False)
        self.chart.setTitle("Income Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")

        self.chart.plot(
            _years, _data.values(), _data.keys(), legend_location="upper right"
        )
        self.chart.show(True)

    def AssetContributionTotals(self):
        _years = []

        _data = {}
        for _record in self.parent.projectionData:
            if _record.clientIsAlive or _record.spouseIsAlive:
                if _record.projectionYear not in _years:
                    _years.append(_record.projectionYear)

                for _name, _value in _record.assetContributions.items():
                    if _name not in _data:
                        _data[_name] = []
                    _data[_name].append(_value)

        # self.chart.show(False)
        self.chart.setTitle("Asset Contribution Totals")
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")

        self.chart.plot(
            _years, _data.values(), _data.keys(), legend_location="upper right"
        )
        self.chart.show(True)
