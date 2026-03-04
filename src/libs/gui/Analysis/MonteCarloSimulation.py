import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from libs.MonteCarloSim import MonteCarloSimulator, StdDevRandomNumberGenerator


class MonteCarloTab(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.dataVariables = None
        # self.text = QPlainTextEdit()

        layout = QVBoxLayout()
        # layout.addWidget(self.text)
        # layout.addWidget(self.table)

        # add a widget to ask for the avg return rate, and std dev
        # add a widget to aks for the avg inflation rate, and std dev.

        # add a button to run the monte carlo sim
        self._button = QPushButton("Run Simulation")
        self._button.clicked.connect(self._run_simulation)
        # add a chart.  #maybe hide the chart until the button is pressed?

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
        for _i in range(_number_of_runs):
            _sim = MonteCarloSimulator(
                _assets_total, _expenses, _avg_returns_generator, _inflation_generator
            )
            _sim.process()
            _balances.append(_sim.get_balances())

            if not _sim.is_bankrupt():
                _success += 1
            else:  # keep track of which step we ran out of money??
                _failure_step.append(_sim.bankrupt_step())

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

    def plot(self, data):
        result = np.array(data).T
        x = np.arange(result.shape[0])
        median = np.median(result, axis=1)
        offsets = (10, 20, 30, 40)

        # print(median)
        # fig, ax = plt.subplots()
        self.canvas.axes.clear()

        def format_dollar(x, pos):
            x = int(x)
            return f"$ {x:,d}"

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_dollar))

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

        self.canvas.draw()
