from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout, QComboBox

from gui.guihelpers.Entry import AgeEntry, PercentEntry


class GlobalVariablesTab(QWidget):
    def __init__(self, parent=None):
        super(GlobalVariablesTab, self).__init__(parent)

        formlayout = QFormLayout()

        self._forecast_years = AgeEntry()  # 2 digit integer
        formlayout.addRow(QLabel("Years to Forecast:"), self._forecast_years)

        self._Inflation = PercentEntry(min=-10.0, max=10.0, num_decimal_places=1)
        formlayout.addRow(QLabel("Inflation:"), self._Inflation)

        self._SS_Cola = PercentEntry(min=0, max=10.0, num_decimal_places=1)
        formlayout.addRow(QLabel("Social Security Cola:"), self._SS_Cola)

        self._WithdrawOrder = QComboBox()
        self._WithdrawOrder.setFixedWidth(200)
        self._WithdrawOrder.addItems(
            [
                "TaxDeferred,Regular,TaxFree",
                "Regular,TaxFree,TaxDeferred",
                "TaxFree, TaxDeferred,Regular",
                "Regular,TaxDeferred,TaxFree",
                "TaxDeferred,TaxFree,Regular",
                "Regular,TaxDeferred,TaxFree",
            ]
        )
        formlayout.addRow(QLabel("Withdrawal Order"), self._WithdrawOrder)

        self.setLayout(formlayout)

    def is_valid(self) -> bool:
        return (
            self._forecast_years.is_valid()
            and self._Inflation.is_valid()
            and self._SS_Cola.is_valid()
        )

    def export_xml(self) -> str:
        return """<GlobalVars>
                 <InflationRate>%s</InflationRate>
                 <SocialSecurityCOLA>%s</SocialSecurityCOLA>
                 <AssetWithdrawOrderByType>%s</AssetWithdrawOrderByType>
                 <YearsToForecast>%s</YearsToForecast>
             </GlobalVars>
       """ % (
            str(self._Inflation.text()),
            str(self._SS_Cola.text()),
            self._WithdrawOrder.currentText(),
            self._forecast_years.text(),
        )

    def import_data(self, inflation: str, SS_COLA, WithdrawOrder, Forecast_years):
        """imports variables to the Global Variables tab"""
        self._Inflation.setText(inflation)
        self._SS_Cola.setText(SS_COLA)
        self._WithdrawOrder.setCurrentText(WithdrawOrder)
        self._forecast_years.setText(Forecast_years)
