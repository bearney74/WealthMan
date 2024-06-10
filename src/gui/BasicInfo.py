#import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
#from tkinter import ttk

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, \
                            QFormLayout, QLineEdit, QComboBox
from PyQt6.QtGui import QIntValidator

import sys
sys.path.append("guihelpers")
from IntegerEntry import IntegerEntry


class BasicInfoTab(QWidget):
  def __init__(self, parent=None):
      super(BasicInfoTab, self).__init__(parent)
      #tk.Frame.__init__(self, parent)

      #self.tk_name=tk.StringVar()
      #self.tk_age=tk.IntVar()
      #self.tk_retirement_age=tk.IntVar()
      #self.tk_lifespan=tk.IntVar()
      #self.tk_lifespan.set(90)  #set default lifespan to 90

      hlayout=QHBoxLayout()
      
      self._clientinfo=PersonBasicInfo("Client", self)
      self._spouseinfo=PersonBasicInfo("Spouse", self)
      self._spouseinfo.setEnabled(False)
 
      hlayout.addWidget(self._clientinfo)
      hlayout.addWidget(self._spouseinfo)
      
      self.setLayout(hlayout)

class PersonBasicInfo(QWidget):
  def __init__(self, person_type:str, parent):
      super(PersonBasicInfo, self).__init__(parent)
      self.parent=parent
      _person_type=person_type
      assert _person_type in ("Client", "Spouse")
      
      vlayout=QVBoxLayout()
      vlayout.addWidget(QLabel("<b>%s Information</b>" % _person_type))
      
      formlayout=QFormLayout()
      vlayout.addLayout(formlayout)
      
      self._name=QLineEdit()
      self._name.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}")
      formlayout.addRow(QLabel("%s Name:" % _person_type), self._name)
      
      self._age=QLineEdit()
      self._age.setMaxLength(2)
      self._age.setValidator(QIntValidator())
      self._age.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}")
      formlayout.addRow(QLabel("%s Age:" % _person_type), self._age)
      
      self._retirement_age=QLineEdit()
      self._retirement_age.setMaxLength(2)
      self._retirement_age.setValidator(QIntValidator())
      self._retirement_age.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}");
      formlayout.addRow(QLabel("%s Retirement Age:" % _person_type), self._retirement_age)
      
      self._lifespan_age=QLineEdit()
      self._lifespan_age.setMaxLength(2)
      self._lifespan_age.setValidator(QIntValidator())
      self._lifespan_age.setStyleSheet("QLineEdit[readOnly=\"true\"] {color: #808080; background-color: #F0F0F0;}");
      formlayout.addRow(QLabel("%s Lifespan Age:" % _person_type), self._lifespan_age)
           
      if _person_type == "Client":
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
      