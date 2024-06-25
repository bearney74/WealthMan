from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox

from PyQt6.QtCore import Qt

from gui.guihelpers.Entry import MoneyEntry, PercentEntry, AgeEntry

from libs.DataVariables import DataVariables, IncomeRecord
from libs.EnumTypes import AccountOwnerType


class IncomeInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(IncomeInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        _layout.addWidget(QLabel("<b><u>Social Security</u></b>"))
        
        _hlayout=QHBoxLayout()
        _glayout=QGridLayout()
        _glayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        _glayout.addWidget(QLabel("Description"), 0, 0)
        _glayout.addWidget(QLabel("FRA Amount"), 0, 1)
        _glayout.addWidget(QLabel("COLA"), 0, 2)
        _glayout.addWidget(QLabel("Begin\nAge"), 0, 3)
        
        _descr = QLineEdit("Client Social Security")
        _descr.setMaximumWidth(300)
        _glayout.addWidget(_descr, 1, 0)
        _glayout.addWidget(MoneyEntry(self.parent), 1, 1)
        _glayout.addWidget(PercentEntry(self.parent), 1, 2)
        _glayout.addWidget(AgeEntry(self.parent), 1, 3)

        _descr = QLineEdit("Spouse Social Security")
        _descr.setMaximumWidth(300)
        _glayout.addWidget(_descr, 2, 0)
        _glayout.addWidget(MoneyEntry(self.parent), 2, 1)
        _glayout.addWidget(PercentEntry(self.parent), 2, 2)
        _glayout.addWidget(AgeEntry(self.parent), 2, 3)
        _hlayout.addLayout(_glayout)
        _hlayout.addStretch()
        
        _layout.addLayout(_hlayout)
        _layout.addStretch(2)
        
        _layout.addWidget(QLabel("<b><u>Pensions</u></b>"))
        
        _hlayout = QHBoxLayout()
        _glayout1=QGridLayout()
        _glayout1.addWidget(QLabel("Description"), 0, 0)
        _glayout1.addWidget(QLabel("Annual Amount"), 0, 1)
        _glayout1.addWidget(QLabel("COLA"), 0, 2)
        _glayout1.addWidget(QLabel("Begin\nAge"), 0, 3)
        _glayout1.addWidget(QLabel("End\nAge"), 0, 4)
        
        _descr = QLineEdit()
        _descr.setMaximumWidth(300)
        _glayout1.addWidget(_descr, 1, 0)
        _glayout1.addWidget(MoneyEntry(self.parent), 1, 1)
        _glayout1.addWidget(PercentEntry(self.parent), 1, 2)
        _glayout1.addWidget(AgeEntry(self.parent), 1, 3)
        _glayout1.addWidget(AgeEntry(self.parent), 1, 4)
        

        _descr = QLineEdit()
        _descr.setMaximumWidth(300)
        _glayout1.addWidget(_descr, 2, 0)
        _glayout1.addWidget(MoneyEntry(self.parent), 2, 1)
        _glayout1.addWidget(PercentEntry(self.parent), 2, 2)
        _glayout1.addWidget(AgeEntry(self.parent), 2, 3)
        _glayout1.addWidget(AgeEntry(self.parent), 2, 4)
        
        _descr = QLineEdit()
        _descr.setMaximumWidth(300)
        _glayout1.addWidget(_descr, 3, 0)
        _glayout1.addWidget(MoneyEntry(self.parent), 3, 1)
        _glayout1.addWidget(PercentEntry(self.parent), 3, 2)
        _glayout1.addWidget(AgeEntry(self.parent), 3, 3)
        _glayout1.addWidget(AgeEntry(self.parent), 3, 4)
        
        _hlayout.addLayout(_glayout1)
        _hlayout.addStretch()
        
        _layout.addLayout(_hlayout)
        _layout.addStretch(2)
        
        #_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        _layout.addWidget(QLabel("<b><u>Other Income Sources: (Full/Part time work)</u></b>"))
        self._add_income_button = QPushButton("Add Income", self)
        self._add_income_button.setFixedSize(90, 30)
        self._add_income_button.clicked.connect(self.add_row)
        _layout.addWidget(self._add_income_button)

        # Table will fit the screen horizontally

        self.gridLayout = QGridLayout()
        _hlayout=QHBoxLayout()
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

            if self.BasicInfoTab.client_is_married():
                self.gridLayout.addWidget(QLabel("Person"), 0, 3)
                self.gridLayout.addWidget(QLabel("Begin Age"), 0, 4)
                self.gridLayout.addWidget(QLabel("End Age"), 0, 5)
            else:
                self.gridLayout.addWidget(QLabel("Begin Age"), 0, 3)
                self.gridLayout.addWidget(QLabel("End Age"), 0, 4)

        _len = self.gridLayout.rowCount()

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
        else:
            _begin_age = AgeEntry(self.parent)
            self.gridLayout.addWidget(_begin_age, _len, 3)

            _end_age = AgeEntry(self.parent)
            self.gridLayout.addWidget(_end_age, _len, 4)

    def clear_form(self):
        for _i in reversed(range(self.gridLayout.count())):
            _item = self.gridLayout.itemAt(_i)
            self.gridLayout.removeItem(_item)
            _item.widget().setParent(None)
            del _item

        assert self.gridLayout.count() == 0

    def export_data(self, dv: DataVariables):
        dv._incomes = []
        for _i in range(1, self.gridLayout.rowCount()):
            _item = self.gridLayout.itemAtPosition(_i, 0)
            print(_i)
            _descr = _item.widget().text()

            _item = self.gridLayout.itemAtPosition(_i, 1)
            _amount = _item.widget().get_int()

            _item = self.gridLayout.itemAtPosition(_i, 2)
            _cola = _item.widget().get_float()

            if self.BasicInfoTab.client_is_married():
                _item = self.gridLayout.itemAtPosition(_i, 3)
                _person = _item.widget().currentText()

                _item = self.gridLayout.itemAtPosition(_i, 4)
                _begin_age = _item.widget().get_int()

                _item = self.gridLayout.itemAtPosition(_i, 5)
                _end_age = _item.widget().get_int()
            else:
                _item = self.gridLayout.itemAtPosition(_i, 3)
                _begin_age = _item.widget().get_int()

                _item = self.gridLayout.itemAtPosition(_i, 4)
                _end_age = _item.widget().get_int()

            _owner = AccountOwnerType.Client
            if self.BasicInfoTab.client_is_married():
                if _person == "Spouse":
                    _owner = AccountOwnerType.Spouse
                    # _owner = "2"

            dv._incomes.append(
                IncomeRecord(_descr, _amount, _cola, _owner, _begin_age, _end_age)
            )

    def import_data(self, d: DataVariables):
        for _record in d._incomes:
            self.add_row()

            _i = self.gridLayout.rowCount() - 1

            _item = self.gridLayout.itemAtPosition(_i, 0)
            _item.widget().setText(_record._descr)

            _item = self.gridLayout.itemAtPosition(_i, 1)
            _item.widget().setText(_record._amount)

            _item = self.gridLayout.itemAtPosition(_i, 2)
            _item.widget().setText(_record._COLA)

            if self.BasicInfoTab.client_is_married():
                if _record._owner == AccountOwnerType.Spouse:
                    _owner = "Spouse"
                else:
                    _owner = "Client"
                _item = self.gridLayout.itemAtPosition(_i, 3)
                _item.widget().setCurrentText(_owner)

                _item = self.gridLayout.itemAtPosition(_i, 4)
                _item.widget().setText(_record._begin_age)

                _item = self.gridLayout.itemAtPosition(_i, 5)
                _item.widget().setText(_record._end_age)
            else:
                _item = self.gridLayout.itemAtPosition(_i, 3)
                _item.widget().setText(_record._begin_age)

                _item = self.gridLayout.itemAtPosition(_i, 4)
                _item.widget().setText(_record._end_age)
