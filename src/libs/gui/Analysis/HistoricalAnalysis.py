import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from libs.HistoricalAnalysis import HistoricalAnalysis, AllocationPeriod


class HistoricalAnalysisTab(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.dataVariables = None
        # self.text = QPlainTextEdit()

        layout = QVBoxLayout()
        # layout.addWidget(self.text)
        # layout.addWidget(self.table)

        # ask for start year and end year (or 1928 to present)

        # add a button to run the monte carlo sim
        self._button = QPushButton("Run Simulation")
        self._button.clicked.connect(self._run_analysis)
        # add a chart.  #maybe hide the chart until the button is pressed?

        layout.addWidget(self._button)

        self._chart = MonteCarloChart(self)
        layout.addWidget(self._chart)
        self.setLayout(layout)

        # self._assets_total=0
        # self._asset_contributions=[]
        # self._expenses=[]

    def _run_single_period(self, begin_year, end_year, balance, incomes, expenses):
        # balance = 100
        # incomes = []
        # expenses = []

        allocationPeriods = [
            AllocationPeriod(0, 10, 80, 15, 5),
            AllocationPeriod(11, 20, 70, 25, 5),
            AllocationPeriod(20, None, 60, 40, 0),
        ]

        # for _i in range(begin_year, end_year + 1):
        #    incomes.append(0)
        #    expenses.append(4)

        _rs = HistoricalAnalysis(
            begin_year,
            end_year,
            incomes,
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
        _incomes = []
        _expenses = []
        for _step, _pyd in enumerate(self.parent.projectionData):
            # _contributions = _pyd.assetContributionTotal.data

            # use incomeSources to get regular income (job, SS, pensions, etc)
            _expense_total = _pyd.expenseTotal.data - _pyd.activeIncomeTotal.data

            # _asset_contributions.append(_contributions)
            _expenses.append(_expense_total)
            _incomes.append(_pyd.activeIncomeTotal.data)

        # _percent_success, _failure_rate=run_simulator(10_000, _assets_total, _expenses)
        _success = 0
        _failure_step = []
        # _results = []
        # retrieve the number of years to of retirement
        _forecast_years = self.dataVariables.forecastYears

        _balances = []
        _begin_year = 1928
        _end_year = 2025
        # _incomes=[0 for _ in range(_forecast_years+1)] #fix me
        for _start_year in range(_begin_year, _end_year - _forecast_years - 1):
            _end_year = _start_year + _forecast_years
            _success, _balance = self._run_single_period(
                _start_year, _end_year, _assets_total, _incomes, _expenses
            )

            _balances.append(_balance)
            # _returns.append(_sim.get_returns())
            # _inflations.append(_sim.get_inflations())

            # if not _sim.is_bankrupt():
            #    _success += 1
            # else:  # keep track of which step we ran out of money??
            # if not _success:
            #    _failure_step.append(_sim.bankrupt_step())

        # _percent_success= 100.0 * _success/float(_number_of_runs)
        # _failure_stats=stats(_failure_step)

        self._chart.plot(_balances)
        self._chart.show(True)
        # print(_failure_step)

        # self.text.setPlainText("Percent Success:%s\nFailure Stats:%s" % (_percent_success, _failure_stats))


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots()
        super(MplCanvas, self).__init__(self.fig)


class MonteCarloChart(QWidget):
    def __init__(self, parent=None):
        super(MonteCarloChart, self).__init__(parent)

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
        # self.canvas.axes2.yaxis.set_major_formatter(FuncFormatter(format_num_obs))
        # self.canvas.axes3.yaxis.set_major_formatter(FuncFormatter(format_num_obs))

    """
    def _set_xaxis_format(self):
        def format_percent(x, pos):
            x=int(x*100.0)
            return f"{x:d}%"
        
        #def format_percent(x, pos):
        #    x=float(x)
        #    return f"{x:3.1f}%"
        
        self.canvas.axes2.xaxis.set_major_formatter(FuncFormatter(format_percent))
        self.canvas.axes3.xaxis.set_major_formatter(FuncFormatter(format_percent))
    """

    def plot(self, balances):

        result = np.array(balances).T
        # x = np.arange(result.shape[0])
        median = np.median(result, axis=1)

        self.canvas.axes.clear()
        self._set_yaxis_format()
        _years = [x for x in range(len(balances[0]))]
        _last = []  # contains the last element in each series
        for _series in balances:
            _last.append(_series[-1])
            self.canvas.axes.plot(_years, _series)

        self.canvas.axes.plot(median, color="black", lw=2)

        self.canvas.axes.axhline(
            y=0, color="gray", linestyle="dashed"
        )  # dashed line at 0

        # self._set_xaxis_format()
        self._set_yaxis_format()

        self.canvas.axes.set_xlim(left=0, right=_years[-1])
        _last.sort()
        _ymax80 = _last[int(len(_last) * 0.98)]
        # print(_ymax80)
        # self.canvas.axes.set_ylim(top=_ymax80)
        self.canvas.axes.set_xlabel("Year")
        # self.canvas.axes.set_ylabel("Dollar")

        """
        #flatten lists
        _returns = [x for x1 in returns for x in x1]
        _inflations = [x for x1 in inflations for x in x1]
        self.canvas.axes2.hist(_returns)
        self.canvas.axes2.set_title("Returns")
        self.canvas.axes3.hist(_inflations)
        self.canvas.axes3.set_title("Inflation")
        """
