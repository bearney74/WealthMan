from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from gui.guihelpers.Entry import MoneyEntry, PercentEntry, AgeEntry

from libs.DataVariables import DataVariables


class AssetInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(AssetInfoTab, self).__init__(parent)

        self.parent = parent
        self.BasicInfoTab = BasicInfoTab

        _layout = QVBoxLayout()

        self._clientinfo = AssetInfoForm(self.parent, "Client")
        self._spouseinfo = AssetInfoForm(self.parent, "Spouse")
        self._spouseinfo.setEnabled(self.BasicInfoTab.client_is_married())

        _layout.addWidget(self._clientinfo)
        _layout.addWidget(self._spouseinfo)

        _layout.addWidget(QLabel("<b><u>Other Assets (Taxable)</u></b>"))

        _flayout = QFormLayout()
        # _layout.addWidget(QLabel("Regular(Taxable):"))
        self.RegularBalance = MoneyEntry()
        _flayout.addRow(QLabel("Regular Balance:"), self.RegularBalance)

        self.RegularCola = PercentEntry()
        _flayout.addRow("Regular COLA:", self.RegularCola)

        self.RegularContribution = AssetContributionForm(self.parent)
        _flayout.addRow(
            QLabel("Regular Annual\nContribution:"), self.RegularContribution
        )

        _layout.addLayout(_flayout)

        _layout.addStretch(2)
        self.setLayout(_layout)

    def clear_form(self):
        self._clientinfo.clear_form()
        self._spouseinfo.clear_form()

        self.RegularBalance.setText("")
        self.RegularCola.setText("")
        self.RegularContribution.clear_form()

    def export_data(self, d: DataVariables):
        d.clientIRABalance = self._clientinfo.IRABalance.get_int()
        d.clientIRACola = self._clientinfo.IRACola.get_float()
        d.clientIRAContribution = (
            self._clientinfo.IRAContribution.Contribution.get_int()
        )
        d.clientIRAContributionBeginAge = (
            self._clientinfo.IRAContribution.BeginAge.get_int()
        )
        d.clientIRAContributionEndAge = (
            self._clientinfo.IRAContribution.EndAge.get_int()
        )

        d.clientRothIRABalance = self._clientinfo.RothIRABalance.get_int()
        d.clientRothIRACola = self._clientinfo.RothIRACola.get_float()
        d.clientRothIRAContribution = (
            self._clientinfo.RothIRAContribution.Contribution.get_int()
        )
        d.clientRothIRAContributionBeginAge = (
            self._clientinfo.RothIRAContribution.BeginAge.get_int()
        )
        d.clientRothIRAContributionEndAge = (
            self._clientinfo.RothIRAContribution.EndAge.get_int()
        )

        if self.BasicInfoTab.client_is_married():
            d.spouseIRABalance = self._spouseinfo.IRABalance.get_int()
            d.spouseIRACola = self._spouseinfo.IRACola.get_float()
            d.spouseIRAContribution = (
                self._spouseinfo.IRAContribution.Contribution.get_int()
            )
            d.spouseIRAContributionBeginAge = (
                self._spouseinfo.IRAContribution.BeginAge.get_int()
            )
            d.spouseIRAContributionEndAge = (
                self._spouseinfo.IRAContribution.EndAge.get_int()
            )

            d.spouseRothIRABalance = self._spouseinfo.RothIRABalance.get_int()
            d.spouseRothIRACola = self._spouseinfo.RothIRACola.get_float()
            d.spouseRothIRAContribution = (
                self._spouseinfo.RothIRAContribution.Contribution.get_int()
            )
            d.spouseRothIRAContributionBeginAge = (
                self._spouseinfo.RothIRAContribution.BeginAge.get_int()
            )
            d.spouseRothIRAContributionEndAge = (
                self._spouseinfo.RothIRAContribution.EndAge.get_int()
            )

        d.regularBalance = self.RegularBalance.get_int()
        d.regularCola = self.RegularCola.get_float()
        d.regularContribution = self.RegularContribution.Contribution.get_int()
        d.regularContributionBeginAge = self.RegularContribution.BeginAge.get_int()
        d.regularContributionEndAge = self.RegularContribution.EndAge.get_int()

    def import_data(self, d: DataVariables):
        self._clientinfo.IRABalance.setText(d.clientIRABalance)
        self._clientinfo.IRACola.setText(d.clientIRACola)
        self._clientinfo.IRAContribution.Contribution.setText(d.clientIRAContribution)
        self._clientinfo.IRAContribution.BeginAge.setText(
            d.clientIRAContributionBeginAge
        )
        self._clientinfo.IRAContribution.EndAge.setText(d.clientIRAContributionEndAge)

        self._clientinfo.RothIRABalance.setText(d.clientRothIRABalance)
        self._clientinfo.RothIRACola.setText(d.clientRothIRACola)
        self._clientinfo.RothIRAContribution.Contribution.setText(
            d.clientRothIRAContribution
        )
        self._clientinfo.RothIRAContribution.BeginAge.setText(
            d.clientRothIRAContributionBeginAge
        )
        self._clientinfo.RothIRAContribution.EndAge.setText(
            d.clientRothIRAContributionEndAge
        )

        self.RegularBalance.setText(d.regularBalance)
        self.RegularCola.setText(d.regularCola)
        # self.RegularContribution.setText(d.regularContribution)
        self.RegularContribution.Contribution.setText(d.regularContribution)
        self.RegularContribution.BeginAge.setText(d.regularContributionBeginAge)
        self.RegularContribution.EndAge.setText(d.regularContributionEndAge)

        self._spouseinfo.IRABalance.setText(d.spouseIRABalance)
        self._spouseinfo.IRACola.setText(d.spouseIRACola)
        # self._spouseinfo.IRAContribution.setText(d.spouseIRAContribution)
        self._spouseinfo.IRAContribution.Contribution.setText(d.spouseIRAContribution)
        self._spouseinfo.IRAContribution.BeginAge.setText(
            d.spouseIRAContributionBeginAge
        )
        self._spouseinfo.IRAContribution.EndAge.setText(d.spouseIRAContributionEndAge)

        self._spouseinfo.RothIRABalance.setText(d.spouseRothIRABalance)
        self._spouseinfo.RothIRACola.setText(d.spouseRothIRACola)
        # self._spouseinfo.RothIRAContribution.setText(d.spouseRothIRAContribution)
        self._spouseinfo.RothIRAContribution.Contribution.setText(
            d.spouseRothIRAContribution
        )
        self._spouseinfo.RothIRAContribution.BeginAge.setText(
            d.spouseRothIRAContributionBeginAge
        )
        self._spouseinfo.RothIRAContribution.EndAge.setText(
            d.spouseRothIRAContributionEndAge
        )


class AssetContributionForm(QWidget):
    def __init__(self, parent):
        super(AssetContributionForm, self).__init__(parent)

        _layout = QHBoxLayout()

        self.Contribution = MoneyEntry()
        _layout.addWidget(self.Contribution)

        _layout.addWidget(QLabel("Begin Age:"))
        self.BeginAge = AgeEntry()
        _layout.addWidget(self.BeginAge)

        self.EndAge = AgeEntry()
        _layout.addWidget(QLabel("End Age:"))
        _layout.addWidget(self.EndAge)
        _layout.addStretch()

        self.setLayout(_layout)

    def clear_form(self):
        self.Contribution.setText("")
        self.BeginAge.setText("")
        self.EndAge.setText("")


class AssetInfoForm(QWidget):
    def __init__(self, parent, person_type):
        super(AssetInfoForm, self).__init__(parent)

        self.parent = parent
        self._person_type = person_type
        # tk.Label(self, text="Client Information").grid(row=_row, column=0, columnspan=2, sticky='w')

        _vlayout = QVBoxLayout()
        _vlayout.addWidget(
            QLabel("<b><u>%s Asset Information</u></b>" % self._person_type)
        )

        _hlayout = QHBoxLayout()
        _flayout = QFormLayout()

        self.IRABalance = MoneyEntry()
        _flayout.addRow(QLabel("IRA Balance:"), self.IRABalance)
        self.IRACola = PercentEntry()
        _flayout.addRow(QLabel("IRA COLA:"), self.IRACola)

        self.IRAContribution = AssetContributionForm(self.parent)
        _flayout.addRow(QLabel("IRA Annual\nContribution:"), self.IRAContribution)
        _hlayout.addLayout(_flayout)

        # _hayout1=QHBoxLayout()
        _flayout1 = QFormLayout()
        self.RothIRABalance = MoneyEntry()
        _flayout1.addRow(QLabel("Roth IRA Balance:"), self.RothIRABalance)

        self.RothIRACola = PercentEntry()
        _flayout1.addRow(QLabel("Roth IRA COLA:"), self.RothIRACola)

        # self.RothIRAContribution = MoneyEntry()
        self.RothIRAContribution = AssetContributionForm(self.parent)
        _flayout1.addRow(
            QLabel("RothIRA Annual\nContribution:"), self.RothIRAContribution
        )

        _hlayout.addLayout(_flayout1)
        _vlayout.addLayout(_hlayout)

        _vlayout.addStretch()

        self.setLayout(_vlayout)

    def clear_form(self):
        self.IRABalance.setText("")
        self.IRACola.setText("")
        self.IRAContribution.clear_form()

        self.RothIRABalance.setText("")
        self.RothIRACola.setText("")
        self.RothIRAContribution.clear_form()
