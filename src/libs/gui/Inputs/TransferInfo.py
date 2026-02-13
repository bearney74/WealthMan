from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox

from PyQt6.QtCore import Qt

from gui.guihelpers.Entry import MoneyEntry, PercentEntry, AgeEntry, PersonTypeEntry

from libs.DataVariables import DataVariables, TransferRecord
# from libs.EnumTypes import AccountOwnerType


class TransferInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(TransferInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._add_transfer_button = QPushButton("Add Tranfer", self)
        self._add_transfer_button.setFixedSize(90, 30)
        self._add_transfer_button.clicked.connect(self.add_row)
        _layout.addWidget(self._add_transfer_button)

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
            self.gridLayout.addWidget(QLabel("Transfer Name"), 0, 0)
            self.gridLayout.addWidget(QLabel("Source Account"), 0, 1)
            self.gridLayout.addWidget(QLabel("Target Account"), 0, 2)

            self.gridLayout.addWidget(QLabel("Annual Amount"), 0, 3)
            _temp = QLabel("Annual\nPercent\nIncrease", wordWrap=True)
            self.gridLayout.addWidget(_temp, 0, 4)

            self.gridLayout.addWidget(QLabel("Person"), 0, 5)
            self.gridLayout.addWidget(QLabel("Begin Age"), 0, 6)
            self.gridLayout.addWidget(QLabel("End Age"), 0, 7)

        _len = self.gridLayout.count() // 8
        _descr = QLineEdit()
        _descr.setMaximumWidth(300)
        self.gridLayout.addWidget(_descr, _len, 0)

        _accounts = ["Client Trad IRA", "Client Roth IRA"]
        if self.BasicInfoTab.client_is_married():
            _accounts += ["Spouse Trad IRA", "Spouse Roth IRA"]

        _accounts += ["Regular Taxable"]

        # put Select Box here for Source Account
        _src_acct = QComboBox()
        _src_acct.addItems(_accounts)
        self.gridLayout.addWidget(_src_acct, _len, 1)

        # put Select Box here for Target Account
        _tgt_acct = QComboBox()
        _tgt_acct.addItems(_accounts)
        self.gridLayout.addWidget(_tgt_acct, _len, 2)

        # Amount
        self.gridLayout.addWidget(MoneyEntry(self.parent), _len, 3)

        # COLA
        self.gridLayout.addWidget(PercentEntry(self.parent), _len, 4)

        # person (Client, Spouse)
        self.gridLayout.addWidget(PersonTypeEntry(self.parent), _len, 5)

        # beginAge
        self.gridLayout.addWidget(AgeEntry(self.parent), _len, 6)

        # endAge
        self.gridLayout.addWidget(AgeEntry(self.parent), _len, 7)

    def clear_form(self):
        _item = self.gridLayout.takeAt(0)
        while _item is not None:
            _item.widget().deleteLater()
            self.gridLayout.removeWidget(_item.widget())
            self.gridLayout.removeItem(_item)
            del _item
            _item = self.gridLayout.takeAt(0)

        self.gridLayout.invalidate()

        assert self.gridLayout.count() == 0

    def export_data(self, d: DataVariables):
        _row = self.gridLayout.count() // 8
        for _i in range(1, _row):
            _item = self.gridLayout.itemAtPosition(_i, 0)
            _descr = _item.widget().text()

            _item = self.gridLayout.itemAtPosition(_i, 1)
            _src_acct = _item.widget().currentText()

            _item = self.gridLayout.itemAtPosition(_i, 2)
            _tgt_acct = _item.widget().currentText()

            _item = self.gridLayout.itemAtPosition(_i, 3)
            _amount = _item.widget().get_int()

            _item = self.gridLayout.itemAtPosition(_i, 4)
            _cola = _item.widget().get_float()

            _item = self.gridLayout.itemAtPosition(_i, 5)
            _person = _item.widget().get()

            _item = self.gridLayout.itemAtPosition(_i, 6)
            _beginYear = _item.widget().get_int()

            _item = self.gridLayout.itemAtPosition(_i, 7)
            _endYear = _item.widget().get_int()

            d.transfers.append(
                TransferRecord(
                    _descr,
                    _src_acct,
                    _tgt_acct,
                    _amount,
                    _cola,
                    _person,
                    _beginYear,
                    _endYear,
                )
            )

    def import_data(self, d: DataVariables):
        for _record in d.transfers:
            self.add_row()

            _i = (self.gridLayout.count() // 8) - 1
            _item = self.gridLayout.itemAtPosition(_i, 0)
            _item.widget().setText(_record.descr)

            _item = self.gridLayout.itemAtPosition(_i, 1)
            _item.widget().setCurrentText(_record.src_acct)

            _item = self.gridLayout.itemAtPosition(_i, 2)
            _item.widget().setCurrentText(_record.tgt_acct)

            _item = self.gridLayout.itemAtPosition(_i, 3)
            _item.widget().setText(_record.amount)

            _item = self.gridLayout.itemAtPosition(_i, 4)
            _item.widget().setText(_record.COLA)

            # person
            _item = self.gridLayout.itemAtPosition(_i, 5)
            _item.widget().set(_record.person)

            _item = self.gridLayout.itemAtPosition(_i, 6)
            _item.widget().setText(_record.beginAge)

            _item = self.gridLayout.itemAtPosition(_i, 7)
            _item.widget().setText(_record.endAge)
