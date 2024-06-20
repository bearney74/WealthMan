from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout, QComboBox

from PyQt6.QtCore import Qt

from gui.guihelpers.Entry import MoneyEntry, PercentEntry, AgeEntry


class ExpenseInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(ExpenseInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent
        
        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._add_expense_button = QPushButton("Add Expense", self)
        self._add_expense_button.setFixedSize(90, 30)
        self._add_expense_button.clicked.connect(self.add_row)
        _layout.addWidget(self._add_expense_button)

        # Table will fit the screen horizontally

        self.gridLayout = QGridLayout()
        _layout.addLayout(self.gridLayout)
        self.setLayout(_layout)

    def add_row(self):
        if self.gridLayout.count() ==0:
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



class ExpenseRecord:
    def __init__(self, descr, amount, percent, person, begin_age, end_age):
        self._descr = descr
        self._amount = amount
        self._percent = percent
        self._person = person
        self._begin_age = begin_age
        self._end_age = end_age
