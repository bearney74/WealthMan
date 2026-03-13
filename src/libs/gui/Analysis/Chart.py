from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox

from ...Projections import DataItem
from .ChartBase import LineChart, FuncFormatter


class Chart(LineChart):
    def __init__(self, parent, width=5, height=45, dpi=100):
        # super(Chart, self).__init__(parent)
        super().__init__(parent)

    # fix me....  Is there a better way to do this?
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
        _data = self.parent.tableData.get_chart_data()
        _categories = []
        for _key, _dataItem in _data[0].items():
            # print(_dataItem)
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
            _chart_data = []
            for _record in _data:
                _chart_data.append(
                    (_record["projectionYear"].data, _record[_variable_name].data)
                )

            self.chart.setTitle(_category)
            self.chart.setLabels(_category)
            if self.parent.tableData.InTodaysDollars:
                self.chart.setSubTitle("In Today's Dollars")

            self.chart.plot(_chart_data)
            self.chart.show(True)
