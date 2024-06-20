import datetime

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
)

from gui.guihelpers.Entry import AgeEntry
from libs.EnumTypes import RelationStatus

class BasicInfoTab(QWidget):
    def __init__(self, parent=None):
        super(BasicInfoTab, self).__init__(parent)
        self.parent=parent
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
        return RelationStatus[self._clientinfo._status.currentText()] == RelationStatus.Married
        
    def clear_form(self):
        self._clientinfo.clear_form()
        if self._spouseinfo is not None:
            self._spouseinfo.clear_form()

    def export_xml(self):
        if self.client_is_married():
            return """<People RelationStatus="Married">%s %s</People>""" % (
                self._clientinfo.export_xml(),
                self._spouseinfo.export_xml(),
            )

        return """<People RelationStatus="Single">%s</People>""" % (
            self._clientinfo.export_xml()
        )

    def import_data(self, num, Name, Age, Retirement_Age, Lifespan_Age, Relationship):
        if num == "1":
            self._clientinfo.import_data(
                Name, Age, Retirement_Age, Lifespan_Age, Relationship
            )
        if num == "2":
            self._spouseinfo.import_data(
                Name, Age, Retirement_Age, Lifespan_Age, Relationship
            )


class PersonBasicInfo(QWidget):
    def __init__(self, person_type: str, parent):
        super(PersonBasicInfo, self).__init__(parent)
        self.parent = parent
        self._person_type = person_type
        assert self._person_type in ("Client", "Spouse")

        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel("<b>%s Information</b>" % self._person_type))

        formlayout = QFormLayout()
        vlayout.addLayout(formlayout)

        self._name = QLineEdit()
        formlayout.addRow(QLabel("%s Name:" % self._person_type), self._name)

        self._age = AgeEntry()
        formlayout.addRow(QLabel("%s Age:" % self._person_type), self._age)

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
        self.parent._spouseinfo.setEnabled(RelationStatus[self._status.currentText()] == RelationStatus.Married)

    def validate_form(self) -> bool:
        if not self.is_valid():
            self.parent.parent.tabs.setCurrentIndex(0)
        
            self._age.setProperty("invalid", True)
            #self._age.setStyleSheet("background-color: red")
            self._name.setText("invalid")
            #self._name.setProperty("invalid", self._name.text().strip() == "")
            #self._age.setProperty("invalid", not self._age.is_valid())
            self._lifespan_age.setProperty("invalid", self._valid_lifespan_age())
            self._retirement_age.setProperty("invalid", self._valid_retirement_age())
            return False

        return True

    def _valid_lifespan_age(self) -> bool:
        _age=self._age.get_int()
        _lage = self._lifespan_age.get_int()
        
        if _lage is None:
           return False
        
        if _age is None:   #assume lifespan is valid is age is missing
            return True
        
        #if we got here we have a lifespan and age.. so lets compare
        if _age >= _lifespan_age:
            return False
        
        _rage = self._retirement_age.get_int()
        
        if _rage is None:  #assume lifespan is valid since retirement age is missing
            return True
            
        return _rage < _lage   #retirement age should be less than lifespan
    
    def _valid_retirement_age(self) -> bool:
        _age=self._age.get_int()
        _rage = self._retirement_age.get_int()
        
        if _rage is None:
           return False
        
        if _age is None:   #assume retirement age is valid is age is missing
            return True
        
        _lage = self._lifespan_age.get_int()
        
        if _lage is None:  #assume retirement age is valid since lifespan age is missing
            return True
            
        return _rage < _lage   #retirement age should be less than lifespan
    
    def is_valid(self) -> bool:
        if self._name.text().strip() == "":
            return False

        return (
            self._age.is_valid()
            and self._valid_lifespan_age()
            and self._valid_retirement_age()
        )

    def clear_form(self):
        self._name.setText("")
        self._age.setText("")
        self._retirement_age.setText("")
        self._lifespan_age.setText("")

        if self._person_type == "Client":
            self._status.setCurrentText("Single")

    def export_xml(self):
        _current_year = datetime.now().year
        _birth_year = _current_year - self._age.get_int()
        _birthdate = "01/01/%s" % _birth_year
        _lifespan = "01/01/%s" % (_birth_year + self._life_span_age.get_int())
        _retirement = "01/01/%s" % (_birth_year + self._retirement_age.get_int())
        return """<Person Num="1" Name="%s" BirthDate="%s" Relationship="Spouse"
                 LifeExpectancy="%s" RetirementDate="%s" />
              """ % (self._name.text(), _birthdate, _lifespan, _retirement)

    def import_data(self, Name, Age, RetirementAge, LifespanAge, Relationship):
        self._name.setText(Name)
        self._age.setText(Age)
        self._retirement_age.setText(RetirementAge)
        self._lifespan_age.setText(LifespanAge)

        if self._person_type == "Client":
            # print(Relationship)
            self._status.setCurrentText(Relationship)
