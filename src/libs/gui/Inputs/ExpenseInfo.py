from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from libs.gui.guihelpers.CustomTableWidgets import ExpenseSourceTableWidget
from libs.DataVariables import DataVariables, ExpenseRecord


class ExpenseInfoTab(QWidget):
    def __init__(self, parent, BasicInfoTab):
        super(ExpenseInfoTab, self).__init__(parent)

        self.BasicInfoTab = BasicInfoTab
        self.parent = parent

        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.table = ExpenseSourceTableWidget(self)
        self.table.addRow()

        _layout.addWidget(self.table)
        _layout.addStretch(3)
        self.setLayout(_layout)

    def validate_form(self) -> bool:
        return self.table.validate_form()

    def clear_form(self):
        self.table.clear()

    def export_data(self, d: DataVariables):
        for (
            _descr,
            _amount,
            _cola,
            _person,
            _begin_age,
            _end_age,
        ) in self.table.getData():
            d.expenses.append(
                ExpenseRecord(_descr, _amount, _cola, _person, _begin_age, _end_age)
            )

    def import_data(self, d: DataVariables):
        self.table.setRowCount(0)
        self.table.setHeader()  # add header back since setRowCount removes the header..

        for _r in d.expenses:
            self.table.addRow(
                [_r.descr, _r.amount, _r.COLA, _r.owner, _r.begin_age, _r.end_age]
            )

        # add an extra row for user input (this row will be blank)..
        self.table.addRow()
