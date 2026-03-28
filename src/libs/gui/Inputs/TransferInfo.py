from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox

from PyQt6.QtCore import Qt

from libs.gui.guihelpers.Entry import (
    MoneyEntry,
    PercentEntry,
    AgeEntry,
    PersonTypeEntry,
)

from libs.gui.guihelpers.DeleteRowGridLayout import DeleteRowGridLayout
from libs.DataVariables import DataVariables, TransferRecord


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
        self.gridLayout = DeleteRowGridLayout(self)  # QGridLayout()
        self.gridLayout.set_header(
            [
                "Transfer Name",
                "Source Account",
                "Target Account",
                "Annual Amount",
                "Annual\nPercent\nIncrease",
                "Person",
                "Begin Age",
                "End Age",
            ]
        )
        _hlayout = QHBoxLayout()
        _hlayout.addLayout(self.gridLayout)
        _hlayout.addStretch()
        _layout.addLayout(_hlayout)
        _layout.addStretch(3)
        self.setLayout(_layout)

    def add_row(self):
        _descr = QLineEdit()
        _descr.setMaximumWidth(400)
        # self.gridLayout.addWidget(_descr, _len, 0)

        _accounts = ["Client Trad IRA", "Client Roth IRA"]
        if self.BasicInfoTab.client_is_married():
            _accounts += ["Spouse Trad IRA", "Spouse Roth IRA"]

        _accounts += ["Regular Taxable"]

        # put Select Box here for Source Account
        _src_acct = QComboBox()
        _src_acct.addItems(_accounts)
        # self.gridLayout.addWidget(_src_acct, _len, 1)

        # put Select Box here for Target Account
        _tgt_acct = QComboBox()
        _tgt_acct.addItems(_accounts)
        # self.gridLayout.addWidget(_tgt_acct, _len, 2)

        _amount = MoneyEntry(self.parent)
        _COLA = PercentEntry(self.parent)
        _owner = PersonTypeEntry(self.parent)
        _begin_age = AgeEntry(self.parent)
        _end_age = AgeEntry(self.parent)

        self.gridLayout.add_row(
            [_descr, _src_acct, _tgt_acct, _amount, _COLA, _owner, _begin_age, _end_age]
        )

    def clear_form(self):
        self.gridLayout.clear()
        # _item = self.gridLayout.takeAt(0)
        # while _item is not None:
        #    _item.widget().deleteLater()
        #    self.gridLayout.removeWidget(_item.widget())
        #    self.gridLayout.removeItem(_item)
        #    del _item
        #    _item = self.gridLayout.takeAt(0)

        # self.gridLayout.invalidate()

        # assert self.gridLayout.count() == 0

    def export_data(self, d: DataVariables):
        for (
            _descr_w,
            _src_acct,
            _tgt_acct,
            _amount_w,
            _cola_w,
            _person_w,
            _begin_age_w,
            _end_age_w,
        ) in self.gridLayout.get_data():
            _descr = _descr_w.text()
            _amount = _amount_w.get_int()
            _cola = _cola_w.get_float()
            _person = _person_w.get()
            _beginAge = _begin_age_w.get_int()
            _endAge = _end_age_w.get_int()

            d.transfers.append(
                TransferRecord(
                    _descr,
                    _src_acct.currentText(),
                    _tgt_acct.currentText(),
                    _amount,
                    _cola,
                    _person,
                    _beginAge,
                    _endAge,
                )
            )

    def _add_row(self, descr, source, target, amount, COLA, person, begin_age, end_age):
        _descr = QLineEdit()
        _descr.setText(descr)
        _descr.setMaximumWidth(400)

        _accounts = ["Client Trad IRA", "Client Roth IRA"]
        if self.BasicInfoTab.client_is_married():
            _accounts += ["Spouse Trad IRA", "Spouse Roth IRA"]

        _accounts += ["Regular Taxable"]

        # put Select Box here for Source Account
        _src_acct = QComboBox()
        _src_acct.addItems(_accounts)
        _src_acct.setCurrentText(source)
        # self.gridLayout.addWidget(_src_acct, _len, 1)

        # put Select Box here for Target Account
        _tgt_acct = QComboBox()
        _tgt_acct.addItems(_accounts)
        _tgt_acct.setCurrentText(target)
        # self.gridLayout.addWidget(_tgt_acct, _len, 2)

        _amount = MoneyEntry(name="Amount", parent=self.parent)
        _amount.setText(amount)

        _COLA = PercentEntry(name="COLA", parent=self.parent)
        _COLA.setText(COLA)

        _person = PersonTypeEntry()
        _person.setEnabled(self.BasicInfoTab.client_is_married())
        _person.set(person)

        _begin_age = AgeEntry(name="Being Age", parent=self.parent)
        _begin_age.setText(begin_age)

        _end_age = AgeEntry(name="End Age", parent=self.parent)
        _end_age.setText(end_age)

        self.gridLayout.add_row(
            [
                _descr,
                _src_acct,
                _tgt_acct,
                _amount,
                _COLA,
                _person,
                _begin_age,
                _end_age,
            ]
        )

    def import_data(self, d: DataVariables):
        for _r in d.transfers:
            self._add_row(
                _r.descr,
                _r.src_acct,
                _r.tgt_acct,
                _r.amount,
                _r.COLA,
                _r.person,
                _r.beginAge,
                _r.endAge,
            )
