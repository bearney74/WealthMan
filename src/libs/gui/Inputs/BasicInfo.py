from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
)

from libs.gui.guihelpers.Entry import (
    AgeEntry,
    DateEntry,
    StringEntry,
    RelationStatusTypeEntry,
)
from libs.gui.guihelpers.Popup import ShowPopup
from libs.gui.guihelpers.FormValidator import FormValidator

from libs.EnumTypes import RelationStatusType, PersonType
from libs.DataVariables import DataVariables


class BasicInfoTab(QWidget):
    def __init__(self, parent=None):
        super(BasicInfoTab, self).__init__(parent)
        self.parent = parent
        hlayout = QHBoxLayout()

        self._clientinfo = PersonBasicInfo(PersonType.CLIENT, self)
        self._spouseinfo = PersonBasicInfo(PersonType.SPOUSE, self)
        self._spouseinfo.setEnabled(False)

        hlayout.addWidget(self._clientinfo)
        hlayout.addWidget(self._spouseinfo)

        self.setLayout(hlayout)

    def validate_form(self):
        if not self.client_is_married():
            return self._clientinfo.validate_form()

        return self._clientinfo.validate_form() and self._spouseinfo.validate_form()

    def is_valid(self) -> bool:
        if not self.client_is_married():
            return self._clientinfo.is_valid()

        return self._clientinfo.is_valid() and self._spouse_info.is_valid()

    def client_is_married(self) -> bool:
        return self._clientinfo._status.get() == RelationStatusType.MARRIED

    def clear_form(self):
        self._clientinfo.clear_form()
        if self._spouseinfo is not None:
            self._spouseinfo.clear_form()

    def export_data(self, d: DataVariables):
        d.clientName = self._clientinfo._name.text()
        d.clientBirthDate = self._clientinfo._birthDate.get_date()
        d.clientLifeSpanAge = self._clientinfo._lifespan_age.get_int()
        d.clientRetirementAge = self._clientinfo._retirement_age.get_int()
        d.relationStatus = self._clientinfo._status.get()  # currentText()

        if self.client_is_married():
            d.spouseName = self._spouseinfo._name.text()
            d.spouseBirthDate = self._spouseinfo._birthDate.get_date()
            d.spouseLifeSpanAge = self._spouseinfo._lifespan_age.get_int()
            d.spouseRetirementAge = self._spouseinfo._retirement_age.get_int()
        else:
            d.spouseName = None
            d.spouseBirthDate = None
            d.spouseLifeSpanAge = None
            d.spouseRetirementAge = None

    def import_data(self, d: DataVariables):
        self._clientinfo.import_data(d)

        if self.client_is_married():
            self._spouseinfo.import_data(d)


class PersonBasicInfo(FormValidator):
    def __init__(self, person_type: PersonType, parent):
        super(PersonBasicInfo, self).__init__(parent)
        # self.parent = parent

        assert isinstance(person_type, PersonType)
        self._person_type = person_type

        _type = person_type.value
        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel("<b><u>%s Information</u></b>" % _type))

        formlayout = QFormLayout()
        vlayout.addLayout(formlayout)

        self._name = StringEntry(name="%s Name" % _type, required=True)
        formlayout.addRow(QLabel("%s Name:" % _type), self._name)

        self._birthDate = DateEntry(self.parent)
        formlayout.addRow(QLabel("%s BirthDate:" % _type), self._birthDate)

        self._retirement_age = AgeEntry(name="%s Retirement Age" % _type, required=True)
        formlayout.addRow(QLabel("%s Retirement Age:" % _type), self._retirement_age)

        self._lifespan_age = AgeEntry(name="%s Lifespan Age" % _type, required=True)
        formlayout.addRow(QLabel("%s Lifespan Age:" % _type), self._lifespan_age)

        if self._person_type == PersonType.CLIENT:
            self._status = RelationStatusTypeEntry()
            self._status.currentIndexChanged.connect(self.selectionchange)
            formlayout.addRow(QLabel("Married Status:"), self._status)

        vlayout.addStretch()

        self.setLayout(vlayout)

        self._name.add_dependencies([self._lifespan_age])
        self._retirement_age.add_dependencies([self._name, self._lifespan_age])
        self._lifespan_age.add_dependencies([self._name])

    def selectionchange(self, i):
        self.parent._spouseinfo.setEnabled(
            self._status.enumValue() == RelationStatusType.MARRIED
        )

    def setEnabled(self, flag: bool):
        super().setEnabled(flag)

        # remove highlight if disabled.
        for _var in (self._name, self._retirement_age, self._lifespan_age):
            _var.set_highlight(flag)
            if flag:
                _var._on_text_change()

    def validate_form(self) -> bool:
        if not self.isEnabled():
            return True

        for _var in (self._name, self._retirement_age, self._lifespan_age):
            if not self.validateEntryWidget(_var):
                return False

        _lage = self._lifespan_age.get_int()
        _rage = self._retirement_age.get_int()
        if _lage <= _rage:
            ShowPopup(
                self,
                "Invalid Input",
                "Lifespan Age (%s) should be greater than Retirement Age (%s)"
                % (_lage, _rage),
            )
            return False

        return True

    def clear_form(self):
        self._name.setText("")
        self._birthDate.clear()
        self._retirement_age.setText("")
        self._lifespan_age.setText("")

        if self._person_type == PersonType.CLIENT:
            self._status.set(RelationStatusType.SINGLE)

    def import_data(self, d: DataVariables):
        if self._person_type == PersonType.CLIENT:
            self._name.setText(d.clientName)
            self._birthDate.set_date(d.clientBirthDate)
            self._lifespan_age.setText(d.clientLifeSpanAge)
            self._retirement_age.setText(d.clientRetirementAge)
            self._status.set(d.relationStatus)
        else:
            self._name.setText(d.spouseName)
            self._birthDate.set_date(d.spouseBirthDate)
            self._lifespan_age.setText(d.spouseLifeSpanAge)
            self._retirement_age.setText(d.spouseRetirementAge)

        # now check that imported data is valid..  hightlight fields if data is not consistent.
        self._name.set_highlight(not self._name.has_valid_input())

        _lage = self._lifespan_age.get_int()
        _rage = self._retirement_age.get_int()

        if _lage is not None and _rage is not None:
            if _lage < _rage:
                self._retirement_age.set_highlight(True)
                self._lifespan_age.set_highlight(True)
                return

        self._retirement_age.set_highlight(not self._retirement_age.has_valid_input())
        self._lifespan_age.set_highlight(not self._lifespan_age.has_valid_input())
