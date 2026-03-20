from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from PyQt6.QtCore import Qt

from libs.gui.guihelpers.Entry import (
    AgeEntry,
    MoneyEntry,
    PercentEntry,
    PersonTypeEntry,
)

from libs.gui.guihelpers.DeleteRowGridLayout import DeleteRowGridLayout

from libs.DataVariables import DataVariables, ExpenseRecord


class ExpenseInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(ExpenseInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._add_expense_button = QPushButton("Add Expense", self)
        self._add_expense_button.setFixedSize(90, 30)
        self._add_expense_button.clicked.connect(self._add_new_row)
        _layout.addWidget(self._add_expense_button)

        # Table will fit the screen horizontally
        self.gridLayout = DeleteRowGridLayout(self)  # QGridLayout()
        self.gridLayout.set_header(
            [
                "Description",
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

    def _add_new_row(self):
        _descr = QLineEdit()
        _descr.setMaximumWidth(400)

        _amount = MoneyEntry(self.parent)

        _COLA = PercentEntry(self.parent)

        _person = PersonTypeEntry()
        _person.setEnabled(self.BasicInfoTab.client_is_married())

        _begin_age = AgeEntry(self.parent)
        _end_age = AgeEntry(self.parent)

        self.gridLayout.add_row([_descr, _amount, _COLA, _person, _begin_age, _end_age])

    def _add_row(self, descr, amount, COLA, person, begin_age, end_age):
        _descr = QLineEdit()
        _descr.setText(descr)
        _descr.setMaximumWidth(400)

        _amount = MoneyEntry(self.parent)
        _amount.setText(amount)

        _COLA = PercentEntry(self.parent)
        _COLA.setText(COLA)

        _person = PersonTypeEntry()
        _person.setEnabled(self.BasicInfoTab.client_is_married())
        _person.set(person)

        _begin_age = AgeEntry(self.parent)
        _begin_age.setText(begin_age)

        _end_age = AgeEntry(self.parent)
        _end_age.setText(end_age)

        self.gridLayout.add_row([_descr, _amount, _COLA, _person, _begin_age, _end_age])

    def clear_form(self):
        self.gridLayout.clear()

    def export_data(self, d: DataVariables):
        for (
            _descr_w,
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
            _begin_age = _begin_age_w.get_int()
            _end_age = _end_age_w.get_int()

            d.expenses.append(
                ExpenseRecord(_descr, _amount, _cola, _person, _begin_age, _end_age)
            )

    def import_data(self, d: DataVariables):
        for _r in d.expenses:
            self._add_row(
                _r.descr, _r.amount, _r.COLA, _r.owner, _r.begin_age, _r.end_age
            )
