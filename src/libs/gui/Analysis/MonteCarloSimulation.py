import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from libs.MonteCarloSim import MonteCarloSimulator, StdDevRandomNumberGenerator, stats


class MonteCarloTab(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.dataVariables = None
        # self.text = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._text_output = QLabel("")

        self._button = QPushButton("Run Simulation")
        self._button.clicked.connect(self._run_simulation)
        # add a chart.  #maybe hide the chart until the button is pressed?

        layout.addWidget(self._text_output)
        layout.addWidget(self._button)

        self._chart = MonteCarloChart(self)
        layout.addWidget(self._chart)
        self.setLayout(layout)

        # self._assets_total=0
        # self._asset_contributions=[]
        # self._expenses=[]

    def _run_simulation(self):
        """calculate total assets as well as expenses and asset contributions for each year"""

        # retrieve the variables we need for the Monte Carlo Simulation
        # we need the total amount of assets
        # we need the total amount of expenses

        _assets_total = self.parent.projectionData[0].assetTotal.data
        _asset_contributions = []
        _expenses = []
        for _step, _pyd in enumerate(self.parent.projectionData):
            _contributions = _pyd.assetContributionTotal.data

            # use incomeSources to get regular income (job, SS, pensions, etc)
            _expense_total = _pyd.expenseTotal.data - _pyd.activeIncomeTotal.data

            _asset_contributions.append(_contributions)
            _expenses.append(_expense_total)

        # _percent_success, _failure_rate=run_simulator(10_000, _assets_total, _expenses)
        _success = 0
        _failure_step = []
        _results = []
        _number_of_runs = self.dataVariables.numberOfRuns
        _avg_returns_generator = StdDevRandomNumberGenerator(
            self.dataVariables.avgROR, self.dataVariables.avgRORStdDev
        )
        _inflation_generator = StdDevRandomNumberGenerator(
            self.dataVariables.avgInflationRate,
            self.dataVariables.avgInflationRateStdDev,
        )

        _balances = []
        _returns = []
        _inflations = []
        for _i in range(_number_of_runs):
            _sim = MonteCarloSimulator(
                _assets_total, _expenses, _avg_returns_generator, _inflation_generator
            )
            _sim.process()
            _balances.append(_sim.get_balances())
            _returns.append(_sim.get_returns())
            _inflations.append(_sim.get_inflations())

            if not _sim.is_bankrupt():
                _success += 1
            else:  # keep track of which step we ran out of money??
                _failure_step.append(_sim.bankrupt_step())

        # _percent_success= 100.0 * _success/float(_number_of_runs)
        # _failure_stats=stats(_failure_step)

        self._text_output.setText(
            "Successful Runs: %s out of %s, (%4.2f%%)"
            % (_success, _number_of_runs, 100.0 * _success / _number_of_runs)
        )
        self._chart.set_subtitle(
            "%4.1f%% Success Rate" % (100.0 * _success / _number_of_runs)
        )
        if len(_failure_step) > 0:
            print(stats(_failure_step))
        # if _number_of_runs >= 1000:
        self._chart.plot(_balances)

        # else:
        #   self._chart.plot2(_balances, _returns, _inflations)
        self._chart.show(True)
        # print(_failure_step)

        # self.text.setPlainText("Percent Success:%s\nFailure Stats:%s" % (_percent_success, _failure_stats))


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots()
        # self.fig = plt.figure()
        # grid = self.fig.add_gridspec(2, 3)
        # self.axes1 = self.fig.add_subplot(grid[:, :-1])  #211
        # self.axes2=self.fig.add_subplot(grid[0,2])    #221
        # self.axes3=self.fig.add_subplot(grid[1,2])    #222
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

        self._subtitle = None

    def set_subtitle(self, subtitle):
        self._subtitle = subtitle

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

    def plot(self, data):
        result = np.array(data).T
        x = np.arange(result.shape[0])
        median = np.median(result, axis=1)
        offsets = (10, 20, 30, 40)

        # print(median)
        # fig, ax = plt.subplots()
        self.canvas.axes.clear()

        self._set_yaxis_format()

        # print(median[-1])
        self.canvas.axes.plot(median, color="black", lw=2)
        for offset in offsets:
            low = np.percentile(result, 50 - offset, axis=1)
            high = np.percentile(result, 50 + offset, axis=1)
            # since `offset` will never be bigger than 50, do 55-offset so that
            # even for the whole range of the graph the fanchart is visible
            alpha = (55 - offset) / 100
            self.canvas.axes.fill_between(x, low, high, color="blue", alpha=alpha)
        self.canvas.axes.legend(["Median"] + [f"Pct{2 * o}" for o in offsets])
        self.canvas.axes.axhline(
            y=0, color="gray", linestyle="dashed"
        )  # dashed line at 0

        self.canvas.axes.set_xlim(left=0, right=len(data[0]) - 1)

        self.canvas.fig.suptitle("Monte Carlo Simulation")
        if self._subtitle is not None:
            self.canvas.fig.text(0.5, 0.9, self._subtitle, horizontalalignment="center")

        self.canvas.draw()

    def plot2(self, balances, returns, inflations):
        self.canvas.axes.clear()
        self._set_yaxis_format()
        _years = [x for x in range(len(balances[0]))]
        _last = []  # contains the last element in each series
        for _series in balances:
            _last.append(_series[-1])
            self.canvas.axes.plot(_years, _series)

        self.canvas.axes.axhline(
            y=0, color="gray", linestyle="dashed"
        )  # dashed line at 0

        # self._set_xaxis_format()
        self._set_yaxis_format()

        self.canvas.axes.set_xlim(left=0, right=_years[-1])
        _last.sort()
        _ymax80 = _last[int(len(_last) * 0.98)]
        # print(_ymax80)
        self.canvas.axes.set_ylim(top=_ymax80)
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
