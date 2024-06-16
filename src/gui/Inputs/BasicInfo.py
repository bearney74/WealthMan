import datetime

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, \
                            QFormLayout, QLineEdit, QComboBox

from gui.guihelpers.Entry import AgeEntry

class BasicInfoTab(QWidget):
  def __init__(self, parent=None):
      super(BasicInfoTab, self).__init__(parent)
      
      hlayout=QHBoxLayout()
      
      self._clientinfo=PersonBasicInfo("Client", self)
      self._spouseinfo=PersonBasicInfo("Spouse", self)
      self._spouseinfo.setEnabled(False)
 
      hlayout.addWidget(self._clientinfo)
      hlayout.addWidget(self._spouseinfo)
      
      self.setLayout(hlayout)
      
  def is_valid(self) -> bool:
      if self._clientinfo._status.currentText() == "Single":
          return self._clientinfo.is_valid()
        
      return self._clientinfo.is_valid() and self._spouse_info.is_valid()
  
  def clear_form(self):
      self._clientinfo.clear_form()
      if self._spouseinfo is not None:
          self._spouseinfo.clear_form()
  
  def export_xml(self):
      if self._clientinfo._status.currentText() == "Married":
         return """<People RelationStatus="Married">%s %s</People>""" % (self._clientinfo.export_xml(), self._spouseinfo.export_xml()) 
                
      return """<People RelationStatus="Single">%s</People>""" % (self._clientinfo.export_xml())
        
  def import_data(self, num, Name, Age, Retirement_Age, Lifespan_Age, Relationship):
      if num == "1":
         self._clientinfo.import_data(Name, Age, Retirement_Age, Lifespan_Age,
                                      Relationship)
      if num == "2":
         self._spouseinfo.import_data(Name, Age, Retirement_Age, Lifespan_Age,
                                      Relationship)
          

class PersonBasicInfo(QWidget):
  def __init__(self, person_type:str, parent):
      super(PersonBasicInfo, self).__init__(parent)
      self.parent=parent
      self._person_type=person_type
      assert self._person_type in ("Client", "Spouse")
      
      vlayout=QVBoxLayout()
      vlayout.addWidget(QLabel("<b>%s Information</b>" % self._person_type))
      
      formlayout=QFormLayout()
      vlayout.addLayout(formlayout)
      
      self._name=QLineEdit()
      self._name.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}")
      formlayout.addRow(QLabel("%s Name:" % self._person_type), self._name)
      
      self._age=AgeEntry()
      self._age.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}")
      formlayout.addRow(QLabel("%s Age:" % self._person_type), self._age)
      
      self._retirement_age=AgeEntry()
      self._retirement_age.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}")
      formlayout.addRow(QLabel("%s Retirement Age:" % self._person_type), self._retirement_age)
      
      self._lifespan_age=AgeEntry()
      self._lifespan_age.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}")
      formlayout.addRow(QLabel("%s Lifespan Age:" % self._person_type), self._lifespan_age)
           
      if self._person_type == "Client":
         self._status=QComboBox()
         self._status.addItems(["Single", "Married"])
         self._status.currentIndexChanged.connect(self.selectionchange)
         formlayout.addRow(QLabel("Married Status:"), self._status)
      
      vlayout.addStretch()

      self.setLayout(vlayout)

  def setEnable(self, value: bool):
      assert isinstance(value, bool)
      self._name.setReadOnly(value)
      self._age.setReadOnly(value)
      self._retirement_age.setReadOnly(value)
      self._lifespan_age.setReadOnly(value)
      
  def selectionchange(self, i):
      self.parent._spouseinfo.setEnabled(self._status.currentText() == "Married")
      
  def is_valid(self) -> bool:
      if self._name.text().strip() == "":
         return False
      
      return self._age.is_valid() and self._life_span.is_valid() and self._retirement_age.is_valid()
      
  def clear_form(self):
      self._name.setText("")
      self._age.setText("")
      self._retirement_age.setText("")
      self._lifespan_age.setText("")
      
      if self._person_type == "Client":
         self._status.setCurrentText("Single")
      
  def export_xml(self):
      _current_year=datetime.now().year
      _birth_year=_current_year - self._age.get_int()
      _birthdate="01/01/%s" % _birth_year
      _lifespan="01/01/%s" % (_birth_year + self._life_span_age.get_int())
      _retirement = "01/01/%s" % (_birth_year + self._retirement_age.get_int())
      return  """<Person Num="1" Name="%s" BirthDate="%s" Relationship="Spouse"
                 LifeExpectancy="%s" RetirementDate="%s" />
              """ % (self._name.text(), _birthdate, _lifespan, _retirement)
    
  def import_data(self, Name, Age, RetirementAge, LifespanAge, Relationship):
      self._name.setText(Name)
      self._age.setText(Age)
      self._retirement_age.setText(RetirementAge)
      self._lifespan_age.setText(LifespanAge)
      
      if self._person_type == "Client":
          #print(Relationship)
          self._status.setCurrentText(Relationship)