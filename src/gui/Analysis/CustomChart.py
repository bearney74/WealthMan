import matplotlib

matplotlib.use("QtAgg")

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import matplotlib.pyplot as plt


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.axes = plt.subplots()
        super(MplCanvas, self).__init__(fig)


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

    def show(self, flag: bool):
        assert isinstance(flag, bool)

        if flag:
            self.canvas.show()
        else:
            self.canvas.hide()

    def plot(self, years, values, labels):
        self.canvas.axes.stackplot(years, values, labels=labels, alpha=0.8)

        self.canvas.axes.set_title(self.title)
        self.canvas.axes.legend(loc="upper left")

        def format_string(x, pos):
            _str = ""
            x = int(x)
            return f"${x:,d}"


class CustomChartTab(QWidget):
    def __init__(self, parent=None):
        super(CustomChartTab, self).__init__(parent)
        self.parent = parent
        # self.Data=[]

        # self.variables=QComboBox(self.parent)

        self.chart = StackChart(self, width=5, height=45, dpi=100)
        # self.chart.show(False)

        layout = QVBoxLayout()
        # hlayout=QHBoxLayout()
        # hlayout.addWidget(self.variables)
        # hlayout.addStretch()
        # layout.addLayout(hlayout)
        layout.addWidget(self.chart)
        self.setLayout(layout)

    def populate(self):
        _years = []

        _data = {}
        _data["Client IRA"] = []
        _data["Client Roth IRA"] = []
        _data["Spouse IRA"] = []
        _data["Spouse Roth IRA"] = []
        _data["Regular"] = []
        for _record in self.parent.projectionData:
            if _record.projectionYear not in _years:
                _years.append(_record.projectionYear)

            for _name, _value in _record.assetSources.items():
                _data[_name].append(_value)

        self.chart.setTitle("Total Assets")
        self.chart.plot(_years, _data.values(), _data.keys())
        self.chart.show(True)
