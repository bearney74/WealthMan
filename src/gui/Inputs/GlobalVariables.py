from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout, QComboBox, QCheckBox

from gui.guihelpers.Entry import AgeEntry, PercentEntry

from libs.DataVariables import DataVariables
from libs.EnumTypes import FederalTaxStatusType


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

        _filing = [
            "Single",
            "MarriedFilingJointly",
            "MarriedFilingSeparately",
            "HeadOfHousehold",
        ]

        self._FilingStatus = QComboBox()
        self._FilingStatus.setFixedWidth(200)
        self._FilingStatus.addItems(_filing)
        formlayout.addRow(QLabel("Federal Filing Status:"), self._FilingStatus)

        self._FilingStatusOnceWidowed = QComboBox()
        self._FilingStatusOnceWidowed.setFixedWidth(200)
        self._FilingStatusOnceWidowed.addItems(_filing)
        formlayout.addRow(
            QLabel("Federal Filing Status once Widowed"), self._FilingStatusOnceWidowed
        )

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
        d.inflation = self._Inflation.get_float(Default=3.0)
        d.withdrawOrder = self._WithdrawOrder.currentText()
        d.forecastYears = self._forecast_years.get_int(Default=30)
        d.inTodaysDollars = self._InTodaysDollars.isChecked()
        d.federalFilingStatus = FederalTaxStatusType[self._FilingStatus.currentText()]
        d.federalFilingStatusOnceWidowed = FederalTaxStatusType[
            self._FilingStatusOnceWidowed.currentText()
        ]

    def import_data(self, d: DataVariables):
        """imports variables to the Global Variables tab"""
        self._Inflation.setText(d.inflation)
        self._WithdrawOrder.setCurrentText(d.withdrawOrder)
        self._forecast_years.setText(d.forecastYears)
        # use hasattr to "upgrade" a saved file to use a new version of
        # WealthMan..  For example, a saved version did not have inTodaysDollars
        # so checking before importing the attribute works.  We could also use
        # the __version__ variable to see what version of WealthMan was saved
        # with and then add default values for new variables
        if hasattr(d, "inTodaysDollars"):
            self._InTodaysDollars.setChecked(d.inTodaysDollars)

        # if hasattr(d, "federalFilingStatus") and d.federalFilingStatus is not None:
        print(d.federalFilingStatus.name)
        self._FilingStatus.setCurrentText(d.federalFilingStatus.name)
        # if hasattr(d, "federalFilingStatusOnceWidowed") and d.federalFilingStatusOnceWidowed is not None:
        self._FilingStatusOnceWidowed.setCurrentText(
            d.federalFilingStatusOnceWidowed.name
        )
