from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout, QComboBox, QCheckBox

from gui.guihelpers.Entry import AgeEntry, PercentEntry

from libs.DataVariables import DataVariables


class GlobalVariablesTab(QWidget):
    def __init__(self, parent=None):
        super(GlobalVariablesTab, self).__init__(parent)

        formlayout = QFormLayout()

        self._forecast_years = AgeEntry()  # 2 digit integer
        formlayout.addRow(QLabel("Years to Forecast:"), self._forecast_years)

        self._Inflation = PercentEntry(min=-10.0, max=10.0, num_decimal_places=1)
        formlayout.addRow(QLabel("Inflation:"), self._Inflation)

        self._WithdrawOrder = QComboBox()
        self._WithdrawOrder.setFixedWidth(200)
        self._WithdrawOrder.addItems(
            [
                "TaxDeferred,Regular,TaxFree",
                "TaxDeferred,TaxFree,Regular",
                "Regular,TaxFree,TaxDeferred",
                "Regular,TaxDeferred,TaxFree",
                "TaxFree, TaxDeferred,Regular",
                "TaxFree,Regular,TaxDeferred",
            ]
        )
        formlayout.addRow(QLabel("Withdrawal Order"), self._WithdrawOrder)

        self._InTodaysDollars = QCheckBox("", self)
        formlayout.addRow(QLabel("In Todays Dollars"), self._InTodaysDollars)

        self.setLayout(formlayout)

    def is_valid(self) -> bool:
        return self._forecast_years.is_valid() and self._Inflation.is_valid()

    def clear_form(self):
        self._WithdrawOrder.setCurrentIndex(0)
        self._forecast_years.setText("")
        self._Inflation.setText("")
        self._InTodaysDollars.setChecked(False)

    def export_data(self, d: DataVariables):
        d.inflation = self._Inflation.get_float()
        d.withdrawOrder = self._WithdrawOrder.currentText()
        d.forecastYears = self._forecast_years.get_int()
        d.inTodaysDollars = self._InTodaysDollars.isChecked()

    def import_data(self, d: DataVariables):
        """imports variables to the Global Variables tab"""
        self._Inflation.setText(d.inflation)
        self._WithdrawOrder.setCurrentText(d.withdrawOrder)
        self._forecast_years.setText(d.forecastYears)
        self._InTodaysDollars.setChecked(d.inTodaysDollars)
