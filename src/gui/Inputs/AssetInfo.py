from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from gui.guihelpers.Entry import MoneyEntry


class AssetInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(AssetInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab

        _layout = QHBoxLayout()

        self._clientinfo = AssetInfoForm(parent, "Client")
        self._spouseinfo = AssetInfoForm(parent, "Spouse")
        self._spouseinfo.setEnabled(
            self.BasicInfoTab.client_is_married()
            #self.BasicInfoTab._clientinfo._status.currentText() == "Married"
        )

        _layout.addWidget(self._clientinfo)
        _layout.addWidget(self._spouseinfo)

        self.setLayout(_layout)


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

        self.Regular = MoneyEntry()
        _layout.addRow(QLabel("Taxable (Regular):"), self.Regular)

        _vlayout.addLayout(_layout)
        _vlayout.addStretch()

        self.setLayout(_vlayout)

    #def setEnable(self, value: bool):
    #    assert isinstance(value, bool)
    #    self.IRA.setReadOnly(value)
    #    self.RothIRA.setReadOnly(value)
    #    self.Regular.setReadOnly(value)
