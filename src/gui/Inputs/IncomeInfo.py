from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout, QComboBox

from PyQt6.QtCore import Qt

from gui.guihelpers.Entry import MoneyEntry, PercentEntry, AgeEntry


class IncomeSourceTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(IncomeSourceTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent
        #self._records = []

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._add_income_button = QPushButton("Add Income", self)
        self._add_income_button.setFixedSize(90, 30)
        self._add_income_button.clicked.connect(self.add_row)
        _layout.addWidget(self._add_income_button)

        # Table will fit the screen horizontally

        #self._num_rows=0
        self.gridLayout = QGridLayout()
        _layout.addLayout(self.gridLayout)
        self.setLayout(_layout)

    def add_row(self):
        if self.gridLayout.count() == 0:
            self.gridLayout.addWidget(QLabel("Description"), 0, 0)
            self.gridLayout.addWidget(QLabel("Annual Amount"), 0, 1)
            _temp = QLabel("Annual\nPercent\nIncrease", wordWrap=True)
            # _temp.setWordWrap(True)
            self.gridLayout.addWidget(_temp, 0, 2)
            
            if self.BasicInfoTab.client_is_married():
               self.gridLayout.addWidget(QLabel("Person"), 0, 3)
            self.gridLayout.addWidget(QLabel("Begin Age"), 0, 4)
            self.gridLayout.addWidget(QLabel("End Age"), 0, 5)

        _len = self.gridLayout.count()

        _descr = QLineEdit()
        _descr.setMaximumWidth(300)
        self.gridLayout.addWidget(_descr, _len, 0)

        _amount = MoneyEntry(self.parent)
        self.gridLayout.addWidget(_amount, _len, 1)

        _percent = PercentEntry(self.parent)
        self.gridLayout.addWidget(_percent, _len, 2)

        if self.BasicInfoTab.client_is_married():
           _person = QComboBox()
           _person.addItems(["Client", "Spouse"])
           self.gridLayout.addWidget(_person, _len, 3)

        _begin_age = AgeEntry(self.parent)
        self.gridLayout.addWidget(_begin_age, _len, 4)

        _end_age = AgeEntry(self.parent)
        self.gridLayout.addWidget(_end_age, _len, 5)

    def clear_form(self):
         
        for _i in reversed(range(self.gridLayout.count())):
            _item=self.gridLayout.itemAt(_i)
            self.gridLayout.removeItem(_item)
            _item.widget().setParent(None)
            del _item

class IncomeRecord:
    def __init__(self, descr, amount, percent, person, begin_age, end_age):
        self._descr = descr
        self._amount = amount
        self._percent = percent
        self._person = person
        self._begin_age = begin_age
        self._end_age = end_age

    def clear_form(self):
        self._descr=""
        self._amount.setText("")
        self._percent.setText("")
        self._person.setIndex(0)
        self._begin_age.setIndex("")
        self._end_age.setIndex("")
        
    def export_xml(self):
        _owner="0"
        if self._person == "Client":
            _owner="1"
        if self._person == "Spouse":
            _owner="2"
        _begin_dt=""
        _end_dt=""
        _str='<Income Name="%s" Amount="%s" AmountPeriod="Annual" ' % (self._descr, self._amount) 
        _str+='       BeginDate="%s" EndDate="%s" COLA="%s" Taxable="Yes" Owner="%s"/>' % (_begin_dt, _end_dt, self._percent, _owner)
                                                                                          
        return _str
    
    def import_data(self, descr, amount, percent, person, begin_dt, end_dt):
        self._descr.setText(descr)
        self._amount.setText(amount)
        self._percent.setText(percent)
        
        if person == "1":
            self._person.setText("Client")
        elif person == "2":
            self._person.setText("Spouse")
            
        self._begin_age.setText("") #begin_dt
        self._end_age.setText("")   #end_dt
        pass