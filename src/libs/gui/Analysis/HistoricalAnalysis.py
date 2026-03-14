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
from libs.gui.guihelpers.Entry import PercentEntry

from .DataTable import DataTableTabBase
from .Charts import MultiLineChart


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

        self._chart = MultiLineChart(self)
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

        self._bt_copy_from_input.clicked.connect(self._copy_from_input)
        glayout.addWidget(self._bt_copy_from_input, 0, 2)

        self._pctBonds = PercentEntry(parent, min=0, max=100, num_decimal_places=0)
        _label = QLabel("Percent Bonds:")
        _label.setFixedWidth(100)
        glayout.addWidget(_label, 1, 0)
        glayout.addWidget(self._pctBonds, 1, 1)

        self._bt_copy_to_input = QPushButton("Copy to Input")
        self._bt_copy_to_input.setMaximumWidth(200)

        self._bt_copy_to_input.clicked.connect(self._copy_to_input)
        glayout.addWidget(self._bt_copy_to_input, 1, 2)

        _hbox = QHBoxLayout()
        _hbox.addLayout(glayout)
        _hbox.addStretch()
        layout.addLayout(_hbox)
        _hbox.setAlignment(glayout, Qt.AlignmentFlag.AlignLeft)

        self._messages = QLabel("")
        layout.addWidget(self._messages)

        self._button = QPushButton("Run Simulation")
        self._button.setMaximumWidth(200)
        self._button.clicked.connect(self._run_analysis)

        layout.addWidget(self._button)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.chartTab = ChartTab(self)
        self.tableTab = DataTableTab(self)
        self.detailedTableTab = DataTableTab(self)
        self.tabs.addTab(self.chartTab, "Chart")
        self.tabs.addTab(self.tableTab, "Data")
        self.tabs.addTab(self.detailedTableTab, "Detailed Data")

        self.tabs.setTabVisible(2, False)

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
        else:
            _pctCash = 100 - _pctStocks - _pctBonds
            self._messages.setText(
                "Pct Stocks: (%s%%), Pct Bonds: (%s%%), Pct Cash: (%s%%)"
                % (_pctStocks, _pctBonds, _pctCash)
            )
            self._messages.setStyleSheet("QLabel {color: black}")

        # for now, one allocation period will work
        # future work.. maybe add additional periods?
        _allocationPeriods = [
            AllocationPeriod(None, None, _pctStocks, _pctBonds, _pctCash)
        ]

        _success = 0
        _failure_step = []
        _forecast_years = self.dataVariables.forecastYears

        _balances = []
        # fix me.. hardcoding end year for now..
        _begin_year = 1928
        _end_year = 2025

        _total = 0
        _count = 0
        _detailed_period_data = []
        _period_datas = []
        for _start_year in range(_begin_year, _end_year - _forecast_years):
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
        _years = [_i for _i in range(len(_balances[0]))]  # number of years..
        _names = [_i for _i in range(len(_balances))]  # can just use numbers
        if False:
            print(len(_years))
            print(len(_balances[0]))
        self.chartTab._chart.setTitle(
            "Historical Analysis (%s to %s)" % (_begin_year, _end_year)
        )
        self.chartTab._chart.setXLabel("Years")
        self.chartTab._chart.setYLabel("Dollars", units="$")
        self.chartTab._chart.plot_data(_years, _balances, _names)
        self.chartTab._chart.show(True)

        _output_detailed = True  # fix me   add a menu bar item to output detailed info for historical Analysis
        self.tabs.setTabVisible(2, _output_detailed)

        if _output_detailed:
            self.detailedTableTab.createTable(_detailed_period_data)

        self.tableTab.createTable(_period_datas)
