from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
    QComboBox,
)

from PyQt6.QtCore import Qt

from gui.guihelpers.Entry import MoneyEntry, PercentEntry, AgeEntry

from libs.DataVariables import DataVariables, IncomeRecord
from libs.EnumTypes import AccountOwnerType


class SocialSecurityWidget(QWidget):
    def __init__(self, parent, person_type):
        super(SocialSecurityWidget, self).__init__(parent)
        self.parent = parent
        self.person_type = person_type

        _layout = QVBoxLayout()
        _flayout = QFormLayout()
        _layout.addWidget(QLabel("%s Social Security" % self.person_type))

        self.Amount = MoneyEntry()
        _label = QLabel("FRA Amount:")
        _label.setToolTip("Full Retirement Age Amount")
        _flayout.addRow(_label, self.Amount)

        self.Cola = PercentEntry(self.parent)
        _label = QLabel("COLA:")
        _label.setToolTip("Cost of Living Adjustment")
        _flayout.addRow(_label, self.Cola)

        self.BeginAge = AgeEntry(min=62, max=70)
        _label = QLabel("Begin Age:")
        _label.setToolTip("Age between 62 and 70")
        _flayout.addRow(_label, self.BeginAge)
        _layout.addLayout(_flayout)

        self.setLayout(_layout)

    def clear_form(self):
        self.Amount.setText("")
        self.Cola.setText("")
        self.BeginAge.setText("")


class IncomeInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(IncomeInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        _layout.addWidget(QLabel("<b><u>Social Security</u></b>"))

        _hlayout = QHBoxLayout()
        self.clientSS = SocialSecurityWidget(self.parent, "Client")
        _hlayout.addWidget(self.clientSS)

        self.spouseSS = SocialSecurityWidget(self.parent, "Spouse")
        _hlayout.addWidget(self.spouseSS)
        self.spouseSS.setEnabled(self.BasicInfoTab.client_is_married())

        _layout.addLayout(_hlayout)
        _layout.addStretch(2)

        _layout.addWidget(QLabel("<b><u>Pensions</u></b>"))

        _hlayout1 = QHBoxLayout()
        _flayout1 = QFormLayout()
        self.pension1Name = QLineEdit()
        self.pension1Name.setMaximumWidth(300)
        _flayout1.addRow(QLabel("Description"), self.pension1Name)

        self.pension1OwnerLabel = QLabel("Owner:")
        self.pension1Owner = QComboBox()
        self.pension1Owner.addItems(["Client", "Spouse"])
        _flayout1.addRow(self.pension1OwnerLabel, self.pension1Owner)

        self.pension1Amount = MoneyEntry()
        _flayout1.addRow(QLabel("Annual Amount:"), self.pension1Amount)

        self.pension1Cola = PercentEntry()
        _flayout1.addRow(QLabel("COLA:"), self.pension1Cola)

        self.pension1SurvivorBenefits = PercentEntry(max=100.0)
        _flayout1.addRow(QLabel("Survivor\nBenefit:"), self.pension1SurvivorBenefits)

        self.pension1BeginAge = AgeEntry()
        _flayout1.addRow(QLabel("Begin Age:"), self.pension1BeginAge)

        self.pension1EndAge = AgeEntry()
        _flayout1.addRow(QLabel("End Age:"), self.pension1EndAge)

        _hlayout1.addLayout(_flayout1)

        _flayout2 = QFormLayout()
        self.pension2Name = QLineEdit()
        self.pension2Name.setMaximumWidth(300)
        _flayout2.addRow(QLabel("Description"), self.pension2Name)

        self.pension2OwnerLabel = QLabel("Owner:")
        self.pension2Owner = QComboBox()
        self.pension2Owner.addItems(["Client", "Spouse"])
        _flayout2.addRow(self.pension2OwnerLabel, self.pension2Owner)

        self.pension2Amount = MoneyEntry()
        _flayout2.addRow(QLabel("Annual Amount:"), self.pension2Amount)

        self.pension2Cola = PercentEntry()
        _flayout2.addRow(QLabel("COLA:"), self.pension2Cola)

        self.pension2SurvivorBenefits = PercentEntry(max=100.0)
        _flayout2.addRow(QLabel("Survivor\nBenefit:"), self.pension2SurvivorBenefits)

        self.pension2BeginAge = AgeEntry()
        _flayout2.addRow(QLabel("Begin Age:"), self.pension2BeginAge)

        self.pension2EndAge = AgeEntry()
        _flayout2.addRow(QLabel("End Age:"), self.pension2EndAge)

        _hlayout1.addLayout(_flayout2)

        _hlayout1.addStretch()

        _layout.addLayout(_hlayout1)
        _layout.addStretch(2)

        _layout.addWidget(
            QLabel("<b><u>Other Income Sources: (Full/Part time work)</u></b>")
        )
        self._add_income_button = QPushButton("Add Income", self)
        self._add_income_button.setFixedSize(90, 30)
        self._add_income_button.clicked.connect(self.add_row)
        _layout.addWidget(self._add_income_button)

        # Table will fit the screen horizontally

        self.gridLayout = QGridLayout()
        _hlayout = QHBoxLayout()
        _hlayout.addLayout(self.gridLayout)
        _hlayout.addStretch()
        _layout.addLayout(_hlayout)
        _layout.addStretch(3)
        self.setLayout(_layout)

    def add_row(self):
        if self.gridLayout.count() == 0:
            self.gridLayout.addWidget(QLabel("Description"), 0, 0)
            self.gridLayout.addWidget(QLabel("Annual Amount"), 0, 1)
            _temp = QLabel("COLA", wordWrap=True)
            self.gridLayout.addWidget(_temp, 0, 2)

            self.gridLayout.addWidget(QLabel("Person"), 0, 3)
            self.gridLayout.addWidget(QLabel("Begin Age"), 0, 4)
            self.gridLayout.addWidget(QLabel("End Age"), 0, 5)

        # do not use rowCount.. it only increases in value
        # even after you delete some elements (ie, rows)
        # _len = self.gridLayout.rowCount()
        _row = self.gridLayout.count() // 6
        # print("line 170, row = ", _row)

        _descr = QLineEdit()
        _descr.setMaximumWidth(300)
        self.gridLayout.addWidget(_descr, _row, 0)

        _amount = MoneyEntry(self.parent)
        self.gridLayout.addWidget(_amount, _row, 1)

        _percent = PercentEntry(self.parent)
        self.gridLayout.addWidget(_percent, _row, 2)

        _person = QComboBox()
        _person.addItems(["Client", "Spouse"])
        self.gridLayout.addWidget(_person, _row, 3)
        _person.setEnabled(self.BasicInfoTab.client_is_married())

        _begin_age = AgeEntry(self.parent)
        self.gridLayout.addWidget(_begin_age, _row, 4)

        _end_age = AgeEntry(self.parent)
        self.gridLayout.addWidget(_end_age, _row, 5)

    def clear_form(self):
        self.clientSS.clear_form()
        self.spouseSS.clear_form()

        # print(self.gridLayout.takeAt(0))
        _item = self.gridLayout.takeAt(0)
        while _item is not None:
            _item.widget().deleteLater()
            self.gridLayout.removeWidget(_item.widget())
            self.gridLayout.removeItem(_item)
            del _item
            _item = self.gridLayout.takeAt(0)

        self.gridLayout.invalidate()

        assert self.gridLayout.count() == 0

    def export_data(self, dv: DataVariables):
        dv.clientSSAmount = self.clientSS.Amount.get_int()
        dv.clientSSCola = self.clientSS.Cola.get_float()
        dv.clientSSBeginAge = self.clientSS.BeginAge.get_int()

        dv.spouseSSAmount = self.spouseSS.Amount.get_int()
        dv.spouseSSCola = self.spouseSS.Cola.get_float()
        dv.spouseSSBeginAge = self.spouseSS.BeginAge.get_int()

        dv.pension1Name = self.pension1Name.text()
        if not self.BasicInfoTab.client_is_married():
            dv.pension1Owner = AccountOwnerType.Client
        else:
            dv.pension1Owner = AccountOwnerType[self.pension1Owner.currentText()]

        dv.pension1Amount = self.pension1Amount.get_int()
        dv.pension1Cola = self.pension1Cola.get_float()
        dv.pension1SurvivorBenefits = self.pension1SurvivorBenefits.get_float()
        dv.pension1BeginAge = self.pension1BeginAge.get_int()
        dv.pension1EndAge = self.pension1EndAge.get_int()

        dv.pension2Name = self.pension2Name.text()
        if not self.BasicInfoTab.client_is_married():
            dv.pension2Owner = AccountOwnerType.Client
        else:
            dv.pension2Owner = AccountOwnerType[self.pension2Owner.currentText()]

        dv.pension2Amount = self.pension2Amount.get_int()
        dv.pension2Cola = self.pension2Cola.get_float()
        dv.pension2SurvivorBenefits = self.pension2SurvivorBenefits.get_float()
        dv.pension2BeginAge = self.pension2BeginAge.get_int()
        dv.pension2EndAge = self.pension2EndAge.get_int()

        dv.otherIncomes = []
        # print(self.gridLayout.count())
        for _row in range(1, self.gridLayout.count() // 6):
            # _row=_i
            _item = self.gridLayout.itemAtPosition(_row, 0)
            _descr = _item.widget().text()

            _item = self.gridLayout.itemAtPosition(_row, 1)
            _amount = _item.widget().get_int()

            _item = self.gridLayout.itemAtPosition(_row, 2)
            _cola = _item.widget().get_float()

            _item = self.gridLayout.itemAtPosition(_row, 3)
            _person = _item.widget().currentText()

            _item = self.gridLayout.itemAtPosition(_row, 4)
            _begin_age = _item.widget().get_int()

            _item = self.gridLayout.itemAtPosition(_row, 5)
            _end_age = _item.widget().get_int()

            _owner = AccountOwnerType.Client
            if self.BasicInfoTab.client_is_married():
                if _person == "Spouse":
                    _owner = AccountOwnerType.Spouse

            dv.otherIncomes.append(
                IncomeRecord(_descr, _amount, _cola, _owner, _begin_age, _end_age)
            )

    def import_data(self, dv: DataVariables):
        self.clientSS.Amount.setText(dv.clientSSAmount)
        self.clientSS.Cola.setText(dv.clientSSCola)
        self.clientSS.BeginAge.setText(dv.clientSSBeginAge)

        self.spouseSS.Amount.setText(dv.spouseSSAmount)
        self.spouseSS.Cola.setText(dv.spouseSSCola)
        self.spouseSS.BeginAge.setText(dv.spouseSSBeginAge)

        self.pension1Name.setText(dv.pension1Name)
        self.pension1Amount.setText(dv.pension1Amount)
        self.pension1Cola.setText(dv.pension1Cola)
        self.pension1SurvivorBenefits.setText(dv.pension1SurvivorBenefits)
        self.pension1BeginAge.setText(dv.pension1BeginAge)
        self.pension1EndAge.setText(dv.pension1EndAge)

        self.pension2Name.setText(dv.pension2Name)
        self.pension2Amount.setText(dv.pension2Amount)
        self.pension2Cola.setText(dv.pension2Cola)
        self.pension2SurvivorBenefits.setText(dv.pension2SurvivorBenefits)
        self.pension2BeginAge.setText(dv.pension2BeginAge)
        self.pension2EndAge.setText(dv.pension2EndAge)

        for _record in dv.otherIncomes:
            self.add_row()

            _row = self.gridLayout.count() // 6 - 1  # need last row number

            _item = self.gridLayout.itemAtPosition(_row, 0)
            _item.widget().setText(_record.descr)

            _item = self.gridLayout.itemAtPosition(_row, 1)
            _item.widget().setText(_record.amount)

            _item = self.gridLayout.itemAtPosition(_row, 2)
            _item.widget().setText(_record.COLA)

            _item = self.gridLayout.itemAtPosition(_row, 3)
            if self.BasicInfoTab.client_is_married():
                if _record.owner == AccountOwnerType.Spouse:
                    _owner = "Spouse"
                else:
                    _owner = "Client"
            else:
                _owner = "Client"
                _item.setEnabled(False)

            _item.widget().setCurrentText(_owner)

            _item = self.gridLayout.itemAtPosition(_row, 4)
            _item.widget().setText(_record.begin_age)

            _item = self.gridLayout.itemAtPosition(_row, 5)
            _item.widget().setText(_record.end_age)
