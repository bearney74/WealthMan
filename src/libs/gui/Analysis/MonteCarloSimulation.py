from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from libs.MonteCarloSim import MonteCarloSimulator, StdDevRandomNumberGenerator, stats
from .Charts import MonteCarloChart


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
        self._button.setMaximumWidth(200)
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
        # fix me   maybe add future incomes?  SS, etc??
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
        _subtitle = "%4.1f%% Success Rate" % (100.0 * _success / _number_of_runs)

        if len(_failure_step) > 1:
            print(stats(_failure_step))
        # if _number_of_runs >= 1000:

        _years = [_i for _i in range(len(_balances[0]))]
        self._chart.setTitle("Monte Carlo Simulation (%s)" % _subtitle)
        self._chart.setXLabel("Year")
        self._chart.setYLabel("Dollars", units="$")
        self._chart.setXRange(0, len(_years), padding=0)

        self._chart.plot_data(_years, _balances)

        self._chart.show(True)
        # print(_failure_step)

        # self.text.setPlainText("Percent Success:%s\nFailure Stats:%s" % (_percent_success, _failure_stats))
