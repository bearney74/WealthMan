from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox

from ...Projections import DataItem
from .Charts import LineChart


class ChartTab(QWidget):
    def __init__(self, parent):
        super(ChartTab, self).__init__(parent)
        self.parent = parent

        self.variables = QComboBox(self.parent)

        self.chart = LineChart(self)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.variables)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addWidget(self.chart)
        self.setLayout(layout)

        self.variables.currentIndexChanged.connect(self._selectionchange)

        self._data = None
        self._variable_map = {}

    def initialize(self):
        if self._data is None:
            self._data = self.parent.tableData.get_chart_data()

            for _name, _dataItem in self._data[0].items():
                if isinstance(_dataItem, DataItem):
                    self._variable_map[_dataItem.header] = _name

    def setCategories(self):
        self.variables.clear()

        self.variables.addItems(list(self._variable_map.keys()))
        self.variables.setCurrentText("Total Assets")

    def _selectionchange(self, i):
        _ndx = self.variables.currentIndex()
        _category = self.variables.currentText()

        # figure out the variable name from the "user friendly" category variable..
        _variable_name = self._variable_map[_category]

        if _variable_name is not None:
            _x = []
            _y = []
            for _record in self._data:
                _x.append(_record["projectionYear"].data)
                _y.append(_record[_variable_name].data)

            self.chart.setTitle(_category)
            self.chart.setXLabel("Year")
            self.chart.setYLabel("Dollars", units="$")
            self.chart.setRightYLabel("Dollars", units="$")

            # fix me currently subtitles don't work well
            if self.parent.tableData.InTodaysDollars:
                self.chart.setSubTitle("In Today's Dollars")

            self.chart.plot_data(_x, _y)
            self.chart.show(True)
