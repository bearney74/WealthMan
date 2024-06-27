from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
)

from gui.guihelpers.Entry import AgeEntry, DateEntry
from libs.EnumTypes import RelationStatus
from libs.DataVariables import DataVariables


class BasicInfoTab(QWidget):
    def __init__(self, parent=None):
        super(BasicInfoTab, self).__init__(parent)
        self.parent = parent
        hlayout = QHBoxLayout()

        self._clientinfo = PersonBasicInfo("Client", self)
        self._spouseinfo = PersonBasicInfo("Spouse", self)
        self._spouseinfo.setEnabled(False)

        hlayout.addWidget(self._clientinfo)
        hlayout.addWidget(self._spouseinfo)

        self.setLayout(hlayout)

    def validate_form(self):
        self._clientinfo.validate_form()
        if self.client_is_married():
            self._spouseinfo.validate_form()

    def is_valid(self) -> bool:
        if not self.client_is_married():
            return self._clientinfo.is_valid()

        return self._clientinfo.is_valid() and self._spouse_info.is_valid()

    def client_is_married(self) -> bool:
        return (
            RelationStatus[self._clientinfo._status.currentText()]
            == RelationStatus.Married
        )

    def clear_form(self):
        self._clientinfo.clear_form()
        if self._spouseinfo is not None:
            self._spouseinfo.clear_form()

    def export_data(self, d: DataVariables):
        d.clientName = self._clientinfo._name.text()
        d.clientBirthDate = self._clientinfo._birthDate.get_date()
        d.clientLifeSpanAge = self._clientinfo._lifespan_age.get_int()
        d.clientRetirementAge = self._clientinfo._retirement_age.get_int()
        d.relationStatus = self._clientinfo._status.currentText()

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
        self._clientinfo._name.setText(d.clientName)
        self._clientinfo._birthDate.set_date(d.clientBirthDate)
        self._clientinfo._lifespan_age.setText(d.clientLifeSpanAge)
        self._clientinfo._retirement_age.setText(d.clientRetirementAge)
        self._clientinfo._status.setCurrentText(d.relationStatus)

        if self.client_is_married():
            self._spouseinfo._name.setText(d.spouseName)
            self._spouseinfo._birthDate.set_date(d.spouseBirthDate)
            self._spouseinfo._lifespan_age.setText(d.spouseLifeSpanAge)
            self._spouseinfo._retirement_age.setText(d.spouseRetirementAge)


class PersonBasicInfo(QWidget):
    def __init__(self, person_type: str, parent):
        super(PersonBasicInfo, self).__init__(parent)
        self.parent = parent
        self._person_type = person_type
        assert self._person_type in ("Client", "Spouse")

        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel("<b><u>%s Information</u></b>" % self._person_type))

        formlayout = QFormLayout()
        vlayout.addLayout(formlayout)

        self._name = QLineEdit()
        formlayout.addRow(QLabel("%s Name:" % self._person_type), self._name)

        self._birthDate = DateEntry(self.parent)
        formlayout.addRow(QLabel("%s BirthDate:" % self._person_type), self._birthDate)

        self._retirement_age = AgeEntry()
        formlayout.addRow(
            QLabel("%s Retirement Age:" % self._person_type), self._retirement_age
        )

        self._lifespan_age = AgeEntry()
        formlayout.addRow(
            QLabel("%s Lifespan Age:" % self._person_type), self._lifespan_age
        )

        if self._person_type == "Client":
            self._status = QComboBox()
            self._status.addItems(["Single", "Married"])
            self._status.currentIndexChanged.connect(self.selectionchange)
            formlayout.addRow(QLabel("Married Status:"), self._status)

        vlayout.addStretch()

        self.setLayout(vlayout)

    def selectionchange(self, i):
        self.parent._spouseinfo.setEnabled(
            RelationStatus[self._status.currentText()] == RelationStatus.Married
        )

    def validate_form(self) -> bool:
        return True
        # TODO: couldnt get this working.. will pass for now and will look at this in the future..
        if not self.is_valid():
            self.parent.parent.tabs.setCurrentIndex(0)

            self._age.setProperty("invalid", True)
            # self._age.setStyleSheet("background-color: red")
            self._name.setText("invalid")
            # self._name.setProperty("invalid", self._name.text().strip() == "")
            # self._age.setProperty("invalid", not self._age.is_valid())
            self._lifespan_age.setProperty("invalid", self._valid_lifespan_age())
            self._retirement_age.setProperty("invalid", self._valid_retirement_age())
            return False

        return True

    def _valid_retirement_age(self) -> bool:
        _rage = self._retirement_age.get_int()

        if _rage is None:
            return False

        _lage = self._lifespan_age.get_int()

        if (
            _lage is None
        ):  # assume retirement age is valid since lifespan age is missing
            return True

        return _rage < _lage  # retirement age should be less than lifespan

    def is_valid(self) -> bool:
        if self._name.text().strip() == "":
            return False

        return self._valid_lifespan_age() and self._valid_retirement_age()

    def clear_form(self):
        self._name.setText("")
        self._birthDate.clear()
        self._retirement_age.setText("")
        self._lifespan_age.setText("")

        if self._person_type == "Client":
            self._status.setCurrentText("Single")
