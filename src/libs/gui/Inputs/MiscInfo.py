from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout, QSpacerItem, QSizePolicy

from libs.gui.guihelpers.Entry import IntegerRangeEntry, FloatEntry, PercentEntry

from libs.DataVariables import DataVariables


class MiscInfoTab(QWidget):
    def __init__(self, parent):
        super(MiscInfoTab, self).__init__(parent)

        self.parent = parent

        formlayout = QFormLayout()

        _title = QLabel("<b><u>Monte Carlo Variables</u></b>")
        formlayout.addRow(_title)
        # Monte Carlo Variables

        self._number_of_runs = IntegerRangeEntry(parent, 100, 10_000, limit_size=50)
        formlayout.addRow(QLabel("Number of Runs:"), self._number_of_runs)

        # avg rate of return
        self._ror = FloatEntry(
            parent, min=0, max=20.0, num_decimal_places=2, limit_size=50
        )
        self._ror.setText(11.85)  # set this each release 1928-2025 avg
        formlayout.addRow(QLabel("Rate of Returns:"), self._ror)

        # std dev
        self._ror_stdDev = FloatEntry(
            parent, min=0, max=30.0, num_decimal_places=2, limit_size=50
        )
        self._ror_stdDev.setText(19.40)  # set this each release 1928-2025 avg
        formlayout.addRow(QLabel("RoR Std. Dev.:"), self._ror_stdDev)

        # avg inflation rate
        self._inflation_rate = FloatEntry(
            parent, min=0, max=6.0, num_decimal_places=2, limit_size=50
        )
        self._inflation_rate.setText(3.11)  # set this each release 1928-2025 avg
        formlayout.addRow(QLabel("Inflation Rate:"), self._inflation_rate)

        # std dev
        self._inflation_stdDev = FloatEntry(
            parent, min=0, max=6.0, num_decimal_places=2, limit_size=50
        )
        self._inflation_stdDev.setText(3.90)  # set this each release 1928-2025 avg
        formlayout.addRow(QLabel("Inflation Std. Dev.:"), self._inflation_stdDev)

        _spacer = QSpacerItem(
            5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        formlayout.addItem(_spacer)

        formlayout.addRow(QLabel("<b><u>Historical Analysis Variables</u></b>"))
        formlayout.addRow(QLabel("Asset Allocation"))

        formlayout.addRow(QLabel("Total of Stocks and Bonds should be <= 100%"))
        formlayout.addRow(QLabel("If total is < 100%, the rest is assumed to be cash."))

        self._pctStocks = PercentEntry(parent, min=0, max=100, num_decimal_places=0)
        formlayout.addRow(QLabel("Percent Stocks:"), self._pctStocks)

        self._pctBonds = PercentEntry(parent, min=0, max=100, num_decimal_places=0)
        formlayout.addRow(QLabel("Percent Bonds:"), self._pctBonds)

        self.setLayout(formlayout)

    def clear_form(self):
        pass

    def export_data(self, d: DataVariables):
        d.numberOfRuns = self._number_of_runs.get_int()
        d.avgROR = self._ror.get_float()
        d.avgRORStdDev = self._ror_stdDev.get_float()
        d.avgInflationRate = self._inflation_rate.get_float()
        d.avgInflationRateStdDev = self._inflation_stdDev.get_float()

        d.pctStocks = self._pctStocks.get_float()
        d.pctBonds = self._pctBonds.get_float()

    def import_data(self, d: DataVariables):
        self._number_of_runs.setText(d.numberOfRuns)
        self._ror.setText(d.avgROR)
        self._ror_stdDev.setText(d.avgRORStdDev)
        self._inflation_rate.setText(d.avgInflationRate)
        self._inflation_stdDev.setText(d.avgInflationRateStdDev)

        self._pctStocks.setText(d.pctStocks)
        self._pctBonds.setText(d.pctBonds)
