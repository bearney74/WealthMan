import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from libs.HistoricalAnalysis import HistoricalAnalysis, AllocationPeriod


class HistoricalAnalysisTab(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.dataVariables = None
        self.projections = None  # an instance of Projections

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ask for start year and end year (or 1928 to present)

        # add a button to run the monte carlo sim
        self._text_output = QLabel("")
        self._button = QPushButton("Run Simulation")
        self._button.clicked.connect(self._run_analysis)

        layout.addWidget(self._text_output)
        layout.addWidget(self._button)

        self._chart = HistoricalAnalysisChart(self)
        layout.addWidget(self._chart)
        self.setLayout(layout)

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
        _success, _balance = _rs.execute()
        return _success, _balance

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

        _success = 0
        _failure_step = []
        _forecast_years = self.dataVariables.forecastYears

        _balances = []
        # fix me..
        _begin_year = 1928
        _end_year = 2025
        _allocationPeriods = [
            AllocationPeriod(0, 10, 80, 15, 5),
            AllocationPeriod(11, 20, 70, 25, 5),
            AllocationPeriod(20, None, 60, 40, 0),
        ]

        _total = 0
        _count = 0
        for _start_year in range(_begin_year, _end_year - _forecast_years - 1):
            _end_year = _start_year + _forecast_years
            _success, _balance = self._run_single_period(
                _start_year,
                _end_year,
                _assets_total,
                _incomes_fixed,
                _incomes_with_COLA,
                _expenses,
                _allocationPeriods,
            )

            _balances.append(_balance)

            _total += 1
            if _success:
                _count += 1

        self._text_output.setText(
            "Successful runs: %s out of %s, (%4.2f%%)"
            % (_count, _total, 100.0 * _count / _total)
        )
        self._chart.plot(_balances)
        self._chart.show(True)


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
                x = int(x / 1_000_000)
                return f"$ {x:,d}M"
            if x > 1_000:
                x = int(x / 1_000)
                return f"$ {x:,d}K"

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
