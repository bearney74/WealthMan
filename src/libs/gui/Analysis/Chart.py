from datetime import datetime
import matplotlib

matplotlib.use("QtAgg")

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots()
        super(MplCanvas, self).__init__(self.fig)


class Chart(QWidget):
    def __init__(self, parent, width=5, height=45, dpi=100):
        super(Chart, self).__init__(parent)
        self.title = ""
        self.subtitle = ""

        _layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=width, height=height, dpi=dpi)
        self.canvas.axes.set_xlabel("Year")
        self.canvas.axes.set_ylabel("Dollars")
        _layout.addWidget(self.canvas)
        self.setLayout(_layout)

    def setLabels(self, category):
        def format_percent(x, pos):
            if isinstance(x, str):
                if x.endswith("%"):
                    x = x[:-1]
                    x = int(x)
            return "%s" % x

        def format_string(x, pos):
            x = int(x)
            return f"{x:,d}"

        match category:
            case (
                "Client RMD %"
                | "Spouse RMD %"
                | "Total RMD %"
                | "Federal Marginal Tax Rate"
                | "Federal Effective Tax Rate"
                | "AWR"
            ):
                self.canvas.axes.set_xlabel("Year")
                self.canvas.axes.set_ylabel("Percent")

                self.canvas.axes.yaxis.set_major_formatter(
                    FuncFormatter(format_percent)
                )

            case _:
                self.canvas.axes.set_xlabel("Year")
                self.canvas.axes.set_ylabel("Dollars")

                self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))

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

    def plot(self, data):
        _x_data = []
        _y_data = []
        for _x, _y in data:
            _x_data.append(_x)
            _y_data.append(_y)

        self.canvas.axes.clear()
        self.canvas.fig.suptitle(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")
        (_line,) = self.canvas.axes.plot(_x_data, _y_data)

        self.setLabels(self.title)

        self.canvas.axes.fill_between(_x_data, 0, _y_data, alpha=0.7)
        _line.figure.canvas.draw()


class ChartTab(QWidget):
    def __init__(self, parent):
        super(ChartTab, self).__init__(parent)
        self.parent = parent

        self.variables = QComboBox(self.parent)

        self.chart = Chart(self, width=5, height=45, dpi=100)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.variables)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addWidget(self.chart)
        self.setLayout(layout)

        self.variables.currentIndexChanged.connect(self._selectionchange)

    def setCategories(self):
        self.variables.clear()
        _categories = self.parent.tableData.getCategories()
        self.variables.addItems(_categories)
        self.variables.setCurrentText("Asset Total")

    def _selectionchange(self, i):
        _ndx = self.variables.currentIndex()

        _data = []
        _year = datetime.now().year  # should we get this somewhere else?
        for _list in self.parent.tableData.data:
            _data.append((_year, _list[_ndx]))
            _year += 1

        _category = self.variables.currentText()
        self.chart.setTitle(_category)
        self.chart.setLabels(_category)
        if self.parent.tableData.InTodaysDollars:
            self.chart.setSubTitle("In Today's Dollars")

        self.chart.plot(_data)
        self.chart.show(True)
