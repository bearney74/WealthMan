import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTabWidget,
    QGridLayout,
)
from PyQt6.QtCore import Qt

from libs.HistoricalAnalysis import HistoricalAnalysis, AllocationPeriod
from libs.Projections import DataItem

from .DataTable import DataTableTabBase
from libs.gui.guihelpers.Entry import PercentEntry


class DataTableTab(DataTableTabBase):
    def __init__(self, parent=None):
        super(DataTableTab, self).__init__(parent)

    def createTable(self, data):
        _data = []
        for _record in data:
            _list = []
            for _attr in _record.__dict__:
                if isinstance(getattr(_record, _attr), DataItem):
                    _list.append(getattr(_record, _attr))

            _data.append(_list)

        _header = [_h.header for _h in _data[0]]
        super(DataTableTab, self).createTable(_header, [], _data)


class ChartTab(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.parent = parent

        layout = QVBoxLayout()
        self._text_output = QLabel("")
        layout.addWidget(self._text_output)
        self._chart = HistoricalAnalysisChart(self)
        layout.addWidget(self._chart)
        self.setLayout(layout)


class HistoricalAnalysisTab(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.dataVariables = None
        self.projections = None  # an instance of Projections

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(QLabel("Total of Stocks and Bonds should be <= 100%"))
        layout.addWidget(
            QLabel("If total is < 100%, the remainder is assumed to be cash.")
        )

        ## ask for start year and end year (or 1928 to present)

        # ask for asset allocation
        glayout = QGridLayout()

        self._pctStocks = PercentEntry(parent, min=0, max=100, num_decimal_places=0)
        _label = QLabel("Percent Stocks:")
        _label.setFixedWidth(100)
        glayout.addWidget(_label, 0, 0)
        glayout.addWidget(self._pctStocks, 0, 1)

        self._bt_copy_from_input = QPushButton("Copy from Input")
        self._bt_copy_from_input.setMaximumWidth(200)

        # self._bt_copy_from_input.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._bt_copy_from_input.clicked.connect(self._copy_from_input)
        glayout.addWidget(self._bt_copy_from_input, 0, 2)

        self._pctBonds = PercentEntry(parent, min=0, max=100, num_decimal_places=0)
        _label = QLabel("Percent Bonds:")
        _label.setFixedWidth(100)
        glayout.addWidget(_label, 1, 0)
        glayout.addWidget(self._pctBonds, 1, 1)

        self._bt_copy_to_input = QPushButton("Copy to Input")
        self._bt_copy_to_input.setMaximumWidth(200)

        # self._bt_copy_to_input.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._bt_copy_to_input.clicked.connect(self._copy_to_input)
        glayout.addWidget(self._bt_copy_to_input, 1, 2)

        # formlayout.addRow(self._bt_copy_from_input, self._bt_copy_to_input)

        _hbox = QHBoxLayout()
        _hbox.addLayout(glayout)
        _hbox.addStretch()
        layout.addLayout(_hbox)  # Qt.AlignmentFlag.AlignLeft)
        # layout.addLayout(glayout) # Qt.AlignmentFlag.AlignLeft)
        _hbox.setAlignment(glayout, Qt.AlignmentFlag.AlignLeft)
        # layout.addStretch()
        # ask if we should output detailed period info
        # self._output_detailed = QCheckBox(text="Output detailed period info?")
        # self._output_detailed.stateChanged.connect(self._toggle_detailed_output)
        # add a button to run simulation
        self._messages = QLabel("")
        layout.addWidget(self._messages)

        self._button = QPushButton("Run Simulation")
        self._button.setMaximumWidth(200)
        self._button.clicked.connect(self._run_analysis)

        # layout.addWidget(self._output_detailed)
        layout.addWidget(self._button)  # , alignment=Qt.AlignmentFlag.AlignLeft)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.chartTab = ChartTab(self)
        self.tableTab = DataTableTab(self)
        self.detailedTableTab = DataTableTab(self)
        self.tabs.addTab(self.chartTab, "Chart")
        self.tabs.addTab(self.tableTab, "Data")
        self.tabs.addTab(self.detailedTableTab, "Detailed Data")

        self.tabs.setTabVisible(2, False)
        # self.detailedTableTab.setVisible(False)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def _copy_to_input(self):
        self.parent.parent.InputsTab.MiscInfoTab._pctStocks.set(
            self._pctStocks.get_float(0)
        )
        self.parent.parent.InputsTab.MiscInfoTab._pctBonds.set(
            self._pctBonds.get_float(0)
        )

    def _copy_from_input(self):
        self._pctStocks.set(
            self.parent.parent.InputsTab.MiscInfoTab._pctStocks.get_float(0.0)
        )
        self._pctBonds.set(
            self.parent.parent.InputsTab.MiscInfoTab._pctBonds.get_float(0.0)
        )

    def _run_single_period(
        self,
        begin_year,
        end_year,
        balance,
        incomes_fixed,
        incomes_with_COLA,
        expenses,
        allocationPeriods,
    ):

        _rs = HistoricalAnalysis(
            begin_year,
            end_year,
            incomes_fixed,
            incomes_with_COLA,
            expenses,
            balance,
            allocationPeriods,
            DefaultReturnRate=5.0,
        )
        _success, _balance, _perioddata, _pd = _rs.execute()
        return _success, _balance, _perioddata, _pd

    def _run_analysis(self):
        """calculate total assets as well as expenses and asset contributions for each year"""

        # retrieve the variables we need for the Monte Carlo Simulation
        # we need the total amount of assets
        # we need the total amount of expenses

        _assets_total = self.parent.projectionData[0].assetTotal.data
        # _asset_contributions = []
        _incomes_fixed = []
        _incomes_with_COLA = []

        _expenses = []
        for _step, _pyd in enumerate(self.parent.projectionData):
            # _contributions = _pyd.assetContributionTotal.data

            # use incomeSources to get regular income (job, SS, pensions, etc)
            _expense_total = _pyd.expenseTotal.data - _pyd.activeIncomeTotal.data

            if _expense_total < 0.0:  # sometimes we may have a surplus of income...
                _expense_total = 0.0
            # _asset_contributions.append(_contributions)
            _expenses.append(_expense_total)

            # need to get to the projections object for the income data since we need
            # more info (ie, does it have a COLA?)
            _fixed = 0
            _with_COLA = 0
            _year = _pyd.projectionYear.data
            for _item in self.projections._IncomeSources:
                if False:
                    print("Year", _year)
                    print(_item.Name)
                    print(_item.BeginDate.year)
                    print(_item.EndDate.year)
                    print(_item.LifeSpanDate.year)
                    print(_item.Amount)
                    print(_item._COLA_Flag)
                if (
                    _item.BeginDate.year <= _year
                    and _item.LifeSpanDate.year >= _year
                    and _item.EndDate.year >= _year
                ):
                    if _item.get_COLA_Flag():
                        _with_COLA += _item.Amount
                    else:
                        _fixed += _item.Amount

            _incomes_fixed.append(_fixed)
            _incomes_with_COLA.append(_with_COLA)

        # retrieve allocation Periods..

        _pctStocks = self._pctStocks.get_float(0)
        _pctBonds = self._pctBonds.get_float(0)

        _pctCash = 0
        if _pctStocks + _pctBonds > 100:
            self._messages.setText(
                # print(
                "Error! Percent Stocks (%s%%) + Percent Bonds (%s%%) > 100.0%%  , Total:(%s%%)"
                % (_pctStocks, _pctBonds, _pctStocks + _pctBonds)
            )
            self._messages.setStyleSheet("QLabel {color: red}")
            return
            # need to product some type of error...
            # _pctStocks = 80
            # _pctBonds = 15
            # _pctCash = 5

        else:
            _pctCash = 100 - _pctStocks - _pctBonds
            self._messages.setText(
                "Pct Stocks: (%s%%), Pct Bonds: (%s%%), Pct Cash: (%s%%)"
                % (_pctStocks, _pctBonds, _pctCash)
            )
            self._messages.setStyleSheet("QLabel {color: black}")

        _allocationPeriods = [
            AllocationPeriod(None, None, _pctStocks, _pctBonds, _pctCash)
        ]

        # print(_expenses)
        _success = 0
        _failure_step = []
        _forecast_years = self.dataVariables.forecastYears

        _balances = []
        # fix me..
        _begin_year = 1928
        _end_year = 2025
        # _allocationPeriods = [
        #    AllocationPeriod(0, 10, 80, 15, 5),
        #    AllocationPeriod(11, 20, 70, 25, 5),
        #    AllocationPeriod(20, None, 60, 40, 0),
        # ]

        _total = 0
        _count = 0
        _detailed_period_data = []
        _period_datas = []
        for _start_year in range(_begin_year, _end_year - _forecast_years - 1):
            _end_year = _start_year + _forecast_years
            _success, _balance, _perioddata, _pd = self._run_single_period(
                _start_year,
                _end_year,
                _assets_total,
                _incomes_fixed,
                _incomes_with_COLA,
                _expenses,
                _allocationPeriods,
            )

            _balances.append(_balance)
            _detailed_period_data += _pd
            _period_datas.append(_perioddata)

            _total += 1
            if _success:
                _count += 1

        self.chartTab._text_output.setText(
            "Successful runs: %s out of %s, (%4.2f%%)"
            % (_count, _total, 100.0 * _count / _total)
        )
        self.chartTab._chart.plot(_balances)
        self.chartTab._chart.show(True)

        _output_detailed = True  # fix me   add a menu bar item to output detailed info for historical Analysis
        self.tabs.setTabVisible(2, _output_detailed)

        if _output_detailed:
            self.detailedTableTab.createTable(_detailed_period_data)

        self.tableTab.createTable(_period_datas)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots()
        super(MplCanvas, self).__init__(self.fig)


class HistoricalAnalysisChart(QWidget):
    def __init__(self, parent=None):
        super(HistoricalAnalysisChart, self).__init__(parent)

        _layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=5, height=45, dpi=100)
        self.canvas.axes.set_xlabel("Year")
        self.canvas.axes.set_ylabel("Dollars")
        _layout.addWidget(self.canvas)
        self.canvas.hide()
        self.setLayout(_layout)

    def show(self, flag: bool):
        assert isinstance(flag, bool)

        if flag:
            self.canvas.show()
        else:
            self.canvas.hide()

    def _set_yaxis_format(self):
        def format_num_obs(x, pos):
            x = int(x / 1000)
            return f"{x:,d}K"

        def format_dollar(x, pos):
            x = int(x)
            if x > 1_000_000:
                x = x / 1_000_000.0
                return f"$ {x:,.1f}M"
            if x > 1_000:
                x = x / 1_000
                return f"$ {x:,.1f}K"

            x = int(x)
            return f"$ {x:,d}"

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_dollar))

    def plot(self, balances):

        result = np.array(balances).T
        median = np.median(result, axis=1)

        self.canvas.axes.clear()
        self._set_yaxis_format()
        _years = [x for x in range(len(balances[0]))]
        for _series in balances:
            self.canvas.axes.plot(_years, _series)

        self.canvas.axes.plot(median, color="black", lw=2)

        self.canvas.axes.axhline(
            y=0, color="gray", linestyle="dashed"
        )  # dashed line at 0

        # self._set_xaxis_format()
        self._set_yaxis_format()

        self.canvas.axes.set_xlim(left=0, right=_years[-1])

        self.canvas.fig.suptitle("Historical Analysis (1928 - present)")
        self.canvas.fig.text(
            0.5, 0.9, "In Today's Dollar", horizontalalignment="center"
        )

        self.canvas.axes.set_xlabel("Year")
        self.canvas.axes.set_ylabel("Dollar")
        self.canvas.draw()
