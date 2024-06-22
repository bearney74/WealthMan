from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from gui.guihelpers.Entry import MoneyEntry

from libs.DataVariables import DataVariables


class AssetInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(AssetInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab

        _layout = QHBoxLayout()

        self._clientinfo = AssetInfoForm(parent, "Client")
        self._spouseinfo = AssetInfoForm(parent, "Spouse")
        self._spouseinfo.setEnabled(
            self.BasicInfoTab.client_is_married()
        )

        _layout.addWidget(self._clientinfo)
        _layout.addWidget(self._spouseinfo)

        self.setLayout(_layout)

    def clear_form(self):
        self._clientinfo.clear_form()
        self._spouseinfo.clear_form()

    def export_data(self, d: DataVariables):
        d._clientIRA = self._clientinfo.IRA.text()
        d._clientRothIRA = self._clientinfo.RothIRA.text()
        d._Regular = self._clientinfo.Regular.text()

        d._spouseIRA = self._spouseinfo.IRA.text()
        d._spouseRothIRA = self._spouseinfo.RothIRA.text()
        # d._spouseRegular=self._spouseinfo._Regular.text()

    def import_data(self, d: DataVariables):
        self._clientinfo.IRA.setText(d._clientIRA)
        self._clientinfo.RothIRA.setText(d._clientRothIRA)
        self._clientinfo.Regular.setText(d._Regular)

        self._spouseinfo.IRA.setText(d._clientIRA)
        self._spouseinfo.RothIRA.setText(d._spouseRothIRA)
        # self._spouseinfo._Regular.setText(d._spouseRegular)


class AssetInfoForm(QWidget):
    def __init__(self, parent, person_type):
        super(AssetInfoForm, self).__init__(parent)

        self._person_type = person_type
        # tk.Label(self, text="Client Information").grid(row=_row, column=0, columnspan=2, sticky='w')

        _vlayout = QVBoxLayout()
        _vlayout.addWidget(QLabel("<b>%s Asset Information</b>" % self._person_type))

        _layout = QFormLayout()
        self.IRA = MoneyEntry()
        _layout.addRow(QLabel("IRA:"), self.IRA)

        self.RothIRA = MoneyEntry()
        _layout.addRow(QLabel("Roth IRA:"), self.RothIRA)

        if self._person_type == "Client":
            self.Regular = MoneyEntry()
            _layout.addRow(QLabel("Taxable (Regular):"), self.Regular)

        _vlayout.addLayout(_layout)
        _vlayout.addStretch()

        self.setLayout(_vlayout)

    def clear_form(self):
        self.IRA.setText("")
        self.RothIRA.setText("")
        if self._person_type == "Client":
            self.Regular.setText("")
