from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)

from PyQt6.QtCore import Qt

from libs.gui.guihelpers.CustomTableWidgets import IncomeSourceTableWidget
from libs.gui.guihelpers.FormValidator import FormValidator
from libs.gui.guihelpers.Entry import (
    AgeEntry,
    MoneyEntry,
    PercentEntry,
    PersonTypeEntry,
    StringEntry,
)
from libs.gui.guihelpers.Popup import ShowPopup

from libs.DataVariables import DataVariables, IncomeRecord
from libs.EnumTypes import PersonType


class SocialSecurityWidget(FormValidator):
    def __init__(self, parent, person_type):
        super(SocialSecurityWidget, self).__init__(parent)

        assert isinstance(person_type, PersonType)
        self.person_type = person_type

        _type = person_type.value  # Client or Spouse
        _layout = QVBoxLayout()
        _flayout = QFormLayout()
        _layout.addWidget(QLabel("%s Social Security" % _type))

        self.Amount = MoneyEntry(name="FRA Amount")
        _label = QLabel("FRA Amount:")
        _label.setToolTip("Full Retirement Age Amount")
        _flayout.addRow(_label, self.Amount)

        self.BeginAge = AgeEntry(name="Begin Age", parent=self, min=62, max=70)
        _label = QLabel("Begin Age:")
        _label.setToolTip("Age between 62 and 70")
        _flayout.addRow(_label, self.BeginAge)
        _layout.addLayout(_flayout)

        self.setLayout(_layout)

        self.Amount.add_dependencies([self.BeginAge])
        self.BeginAge.add_dependencies([self.Amount])

    def clear_form(self):
        self.Amount.setText("")
        self.BeginAge.setText("")

    def validate_form(self) -> bool:
        if not self.isEnabled():
            return True

        for _var in (self.Amount, self.BeginAge):
            if not self.validateEntryWidget(_var):
                return False

        return True


class PensionWidget(FormValidator):
    def __init__(self, parent):
        super(PensionWidget, self).__init__(parent)

        _flayout = QFormLayout()

        self.Name = StringEntry(limit_size=300)
        _flayout.addRow(QLabel("Description"), self.Name)

        self.Owner = PersonTypeEntry()
        _flayout.addRow(QLabel("Owner:"), self.Owner)

        self.Amount = MoneyEntry()
        _flayout.addRow(QLabel("Annual Amount:"), self.Amount)

        self.Cola = PercentEntry()
        _flayout.addRow(QLabel("COLA:"), self.Cola)

        self.SurvivorBenefits = PercentEntry(max=100.0)
        _flayout.addRow(QLabel("Survivor\nBenefit:"), self.SurvivorBenefits)

        self.BeginAge = AgeEntry()
        _flayout.addRow(QLabel("Begin Age:"), self.BeginAge)

        self.EndAge = AgeEntry()
        _flayout.addRow(QLabel("End Age:"), self.EndAge)

        self.setLayout(_flayout)

        # add dependencies (used for input validation)
        self.Name.add_dependencies([self.Amount])
        self.Amount.add_dependencies([self.Name])
        self.Cola.add_dependencies([self.Name, self.Amount])
        self.SurvivorBenefits.add_dependencies([self.Name, self.Amount])
        self.BeginAge.add_dependencies([self.Name, self.Amount])
        self.EndAge.add_dependencies([self.Name, self.Amount])

    def clear_form(self):
        self.Name.setText("")
        self.Owner.set(PersonType.CLIENT)
        self.Amount.setText("")
        self.Cola.setText("")
        self.SurvivorBenefits.setText("")
        self.BeginAge.setText("")
        self.EndAge.setText("")

    def validate_form(self) -> bool:
        for _var in (
            self.Name,
            self.Amount,
            self.Cola,
            self.SurvivorBenefits,
            self.BeginAge,
            self.EndAge,
        ):
            if not self.validateEntryWidget(_var):
                return False

        _begin_age = self.BeginAge.get_int()
        _end_age = self.EndAge.get_int()

        if _begin_age is not None and _end_age is not None:
            if _end_age < _begin_age:
                ShowPopup(
                    self,
                    "Invalid Input",
                    "End Age (%s) should be greater than Begin Age (%s)"
                    % (_end_age, _begin_age),
                )
                return False

        return True


class IncomeInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(IncomeInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        _layout.addWidget(QLabel("<b><u>Social Security</u></b>"))

        _hlayout = QHBoxLayout()
        self.clientSS = SocialSecurityWidget(self.parent, PersonType.CLIENT)
        _hlayout.addWidget(self.clientSS)

        self.spouseSS = SocialSecurityWidget(self.parent, PersonType.SPOUSE)
        _hlayout.addWidget(self.spouseSS)
        self.spouseSS.setEnabled(self.BasicInfoTab.client_is_married())

        _layout.addLayout(_hlayout)
        _layout.addStretch(2)

        _layout.addWidget(QLabel("<b><u>Pensions</u></b>"))

        _hlayout2 = QHBoxLayout()

        self.pension1 = PensionWidget(self)
        _hlayout2.addWidget(self.pension1)

        self.pension2 = PensionWidget(self)
        _hlayout2.addWidget(self.pension2)

        _layout.addLayout(_hlayout2)
        _layout.addStretch(2)

        _layout.addWidget(
            QLabel("<b><u>Other Income Sources: (Full/Part time work)</u></b>")
        )

        self.table = IncomeSourceTableWidget(parent=self)
        self.table.addRow()

        _layout.addWidget(self.table)
        _layout.addStretch(3)
        self.setLayout(_layout)

    def clear_form(self):
        self.clientSS.clear_form()
        self.spouseSS.clear_form()

        self.pension1.clear_form()
        self.pension2.clear_form()

        self.table.clear()

    def validate_form(self):
        _ss_client = self.clientSS.validate_form()
        _ss_spouse = self.spouseSS.validate_form()

        _pension1 = self.pension1.validate_form()
        _pension2 = self.pension2.validate_form()

        _table = self.table.validate_form()

        return _ss_client and _ss_spouse and _pension1 and _pension2 and _table

    def export_data(self, dv: DataVariables):
        dv.clientSSAmount = self.clientSS.Amount.get_int()
        dv.clientSSBeginAge = self.clientSS.BeginAge.get_int()

        dv.spouseSSAmount = self.spouseSS.Amount.get_int()
        dv.spouseSSBeginAge = self.spouseSS.BeginAge.get_int()

        dv.pension1Name = self.pension1.Name.text()
        if not self.BasicInfoTab.client_is_married():
            dv.pension1Owner = PersonType.CLIENT
        else:
            dv.pension1Owner = self.pension1.Owner.get()

        dv.pension1Amount = self.pension1.Amount.get_int()
        dv.pension1Cola = self.pension1.Cola.get_float()
        dv.pension1SurvivorBenefits = self.pension1.SurvivorBenefits.get_float()
        dv.pension1BeginAge = self.pension1.BeginAge.get_int()
        dv.pension1EndAge = self.pension1.EndAge.get_int()

        dv.pension2Name = self.pension2.Name.text()
        if not self.BasicInfoTab.client_is_married():
            dv.pension2Owner = PersonType.CLIENT
        else:
            dv.pension2Owner = self.pension2.Owner.get()

        dv.pension2Amount = self.pension2.Amount.get_int()
        dv.pension2Cola = self.pension2.Cola.get_float()
        dv.pension2SurvivorBenefits = self.pension2.SurvivorBenefits.get_float()
        dv.pension2BeginAge = self.pension2.BeginAge.get_int()
        dv.pension2EndAge = self.pension2.EndAge.get_int()

        dv.otherIncomes = []
        for (
            _descr,
            _amount,
            _cola,
            _owner,
            _begin_age,
            _end_age,
        ) in self.table.getData():
            dv.otherIncomes.append(
                IncomeRecord(_descr, _amount, _cola, _owner, _begin_age, _end_age)
            )

    def import_data(self, dv: DataVariables):
        self.clientSS.Amount.setText(dv.clientSSAmount)
        self.clientSS.BeginAge.setText(dv.clientSSBeginAge)

        self.spouseSS.Amount.setText(dv.spouseSSAmount)
        self.spouseSS.BeginAge.setText(dv.spouseSSBeginAge)

        self.pension1.Name.setText(dv.pension1Name)
        self.pension1.Amount.setText(dv.pension1Amount)
        self.pension1.Cola.setText(dv.pension1Cola)
        self.pension1.SurvivorBenefits.setText(dv.pension1SurvivorBenefits)
        self.pension1.BeginAge.setText(dv.pension1BeginAge)
        self.pension1.EndAge.setText(dv.pension1EndAge)

        self.pension2.Name.setText(dv.pension2Name)
        self.pension2.Amount.setText(dv.pension2Amount)
        self.pension2.Cola.setText(dv.pension2Cola)
        self.pension2.SurvivorBenefits.setText(dv.pension2SurvivorBenefits)
        self.pension2.BeginAge.setText(dv.pension2BeginAge)
        self.pension2.EndAge.setText(dv.pension2EndAge)

        for _record in dv.otherIncomes:
            self.table.addRow(
                [
                    _record.descr,
                    _record.amount,
                    _record.COLA,
                    _record.owner,
                    _record.begin_age,
                    _record.end_age,
                ]
            )
