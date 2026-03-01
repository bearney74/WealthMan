from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout, QCheckBox

from libs.gui.guihelpers.Entry import (
    AgeEntry,
    PercentEntry,
    YearEntry,
    WithdrawOrderEntry,
    FederalTaxStatusEntry,
)

from libs.DataVariables import DataVariables


class GlobalVariablesTab(QWidget):
    def __init__(self, parent=None):
        super(GlobalVariablesTab, self).__init__(parent)

        formlayout = QFormLayout()

        self._start_year = YearEntry()  # 4 digit integer
        formlayout.addRow(QLabel("Start Year:"), self._start_year)

        self._forecast_years = AgeEntry()  # 2 digit integer
        formlayout.addRow(QLabel("Num Years to Forecast:"), self._forecast_years)

        self._Inflation = PercentEntry(min=-10.0, max=10.0, num_decimal_places=1)
        formlayout.addRow(QLabel("Inflation:"), self._Inflation)

        self._ssCola = PercentEntry(min=-10.0, max=10.0, num_decimal_places=1)
        formlayout.addRow(QLabel("SS Cola:"), self._ssCola)

        self._WithdrawOrder = WithdrawOrderEntry(limit_size=250)
        formlayout.addRow(QLabel("Withdrawal Order"), self._WithdrawOrder)

        self._FilingStatus = FederalTaxStatusEntry(limit_size=200)
        formlayout.addRow(QLabel("Federal Filing Status:"), self._FilingStatus)

        self._FilingStatusOnceWidowed = FederalTaxStatusEntry(limit_size=200)
        formlayout.addRow(
            QLabel("Federal Filing Status once Widowed"), self._FilingStatusOnceWidowed
        )

        self._InTodaysDollars = QCheckBox("", self)
        formlayout.addRow(QLabel("In Todays Dollars"), self._InTodaysDollars)

        self._SurplusAccount = QCheckBox("", self)
        formlayout.addRow(
            QLabel("Add surplus to a surplus account:"), self._SurplusAccount
        )
        self._SurplusAccount.clicked.connect(self._enable_disable_surplus_interest)

        self._SurplusAccountInterestRate = PercentEntry(
            min=-10.0, max=10.0, num_decimal_places=1
        )
        formlayout.addRow(
            QLabel("Surplus Account Interest Rate:"), self._SurplusAccountInterestRate
        )
        self._SurplusAccountInterestRate.setEnabled(False)

        self.setLayout(formlayout)

    def _enable_disable_surplus_interest(self, e):
        self._SurplusAccountInterestRate.setEnabled(self._SurplusAccount.isChecked())

    def is_valid(self) -> bool:
        return self._forecast_years.is_valid() and self._Inflation.is_valid()

    def clear_form(self):
        self._start_year.setText("")
        self._WithdrawOrder.setCurrentIndex(0)
        self._forecast_years.setText("")
        self._Inflation.setText("")
        self._ssCola.setText("")
        self._InTodaysDollars.setChecked(False)
        self._SurplusAccount.setChecked(False)
        self._SurplusAccountInterestRate.setText("")

    def export_data(self, d: DataVariables):
        d.start_year = self._start_year.get_int(Default=None)
        d.inflation = self._Inflation.get_float(Default=3.0)
        d.ssCola = self._ssCola.get_float(Default=3.0)
        d.withdrawOrder = self._WithdrawOrder.enumValue()  # currentText()
        d.forecastYears = self._forecast_years.get_int(Default=30)
        d.inTodaysDollars = self._InTodaysDollars.isChecked()
        d.federalFilingStatus = self._FilingStatus.enumValue()
        d.federalFilingStatusOnceWidowed = self._FilingStatusOnceWidowed.enumValue()

        d.SurplusAccount = self._SurplusAccount.isChecked()
        if self._SurplusAccount.isChecked():
            d.SurplusAccountInterestRate = self._SurplusAccountInterestRate.get_float(
                Default=1.0
            )
        else:
            d.SurplusAccountInterestRate = None

    def import_data(self, d: DataVariables):
        """imports variables to the Global Variables tab"""
        self._start_year.setText(d.start_year)
        self._Inflation.setText(d.inflation)
        self._ssCola.setText(d.ssCola)
        self._WithdrawOrder.set(d.withdrawOrder)
        self._forecast_years.setText(d.forecastYears)
        # if hasattr(d, "inTodaysDollars"):
        self._InTodaysDollars.setChecked(d.inTodaysDollars)

        self._FilingStatus.set(d.federalFilingStatus)
        self._FilingStatusOnceWidowed.set(d.federalFilingStatusOnceWidowed)
        self._SurplusAccount.setChecked(d.SurplusAccount)
        self._SurplusAccountInterestRate.setText(d.SurplusAccountInterestRate)
        self._SurplusAccountInterestRate.setEnabled(d.SurplusAccount)
