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

    def setCategories(self):
        self.variables.clear()
        _data = self.parent.tableData.get_chart_data()
        _categories = []
        for _key, _dataItem in _data[0].items():
            if _key != "federalTaxFilingStatus":
                _categories.append(_dataItem.header)

        self.variables.addItems(_categories)
        self.variables.setCurrentText("Total Assets")

    def _selectionchange(self, i):
        _ndx = self.variables.currentIndex()
        _category = self.variables.currentText()
        _data = self.parent.tableData.get_chart_data()

        # figure out the variable name from the "user friendly" category variable..
        _variable_name = None
        for _var_name, _dataItem in _data[0].items():
            if isinstance(_dataItem, DataItem):
                if _category == _dataItem.header:
                    _variable_name = _var_name

        if _variable_name is not None:
            _x = []
            _y = []
            for _record in _data:
                _x.append(_record["projectionYear"].data)
                _y.append(_record[_variable_name].data)

            self.chart.setTitle(_category)
            self.chart.setXLabel("Year")
            self.chart.setYLabel("Dollars", units="$")

            # fix me currently subtitles don't work well
            if self.parent.tableData.InTodaysDollars:
                self.chart.setSubTitle("In Today's Dollars")

            self.chart.plot_data(_x, _y)
            self.chart.show(True)
