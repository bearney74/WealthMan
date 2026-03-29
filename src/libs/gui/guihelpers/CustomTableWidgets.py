from libs.gui.guihelpers.Entry import PersonTypeEntry, AccountEntry

from libs.gui.guihelpers.Popup import ShowPopup
from libs.gui.guihelpers.DeleteRowTableWidget import (
    DeleteRowTableWidget,
    AgeEntryCell,
    MoneyEntryCell,
    PercentEntryCell,
    StringEntryCell,
)


class IncomeSourceTableWidget(DeleteRowTableWidget):
    def __init__(self, parent):
        super(IncomeSourceTableWidget, self).__init__(parent)

        self.setHeader()  # we don't count the "Remove Row" column

        self.setColumnWidth(0, 300)
        self.setColumnWidth(self.numColumns, 50)  # resize remove row

        self._person_enabled: bool = (
            False  # enable/disable PersonTypeEntry (ie, combobox)
        )

    def setHeader(
        self,
    ):  # have to do this since setRowColumn (and clear) remove the headers...
        _header = [
            "Description",
            "Annual Amount",
            "COLA",
            "Person",
            "Begin Age",
            "End Age",
        ]
        super().setHeader(_header)  # we don't count the "Remove Row" column

    def addRow(self, data=[]):
        _row = self.rowCount()

        assert len(data) in (0, self.numColumns)

        # print("insertRow:", _row)
        self.insertRow(_row)
        _descr = StringEntryCell(parent=self, name="Description")
        _amount = MoneyEntryCell(parent=self, name="Annual Amount")
        _cola = PercentEntryCell(parent=self, name="COLA")
        _person = PersonTypeEntry(parent=self)
        _person.setEnabled(self._person_enabled)
        _begin_age = AgeEntryCell(parent=self, name="Begin Age")
        _end_age = AgeEntryCell(parent=self, name="End Age")

        # add any dependencies
        _descr.add_dependencies([_amount])
        _amount.add_dependencies([_descr])
        _cola.add_dependencies([_descr, _amount])
        _begin_age.add_dependencies([_descr, _amount])
        _end_age.add_dependencies([_descr, _amount])

        # add widgets to the row
        self.setCellWidget(_row, 0, _descr)
        self.setCellWidget(_row, 1, _amount)
        self.setCellWidget(_row, 2, _cola)
        self.setCellWidget(_row, 3, _person)
        self.setCellWidget(_row, 4, _begin_age)
        self.setCellWidget(_row, 5, _end_age)

        # add data to the table row if we have data
        # add remove row button to the last column
        self._addRow(_row, data)

    def setEnabledOwner(self, enable: bool) -> None:
        self._person_enabled = enable
        for _row in range(self.rowCount()):
            _persontype = self.cellWidget(_row, 3)
            assert isinstance(_persontype, PersonTypeEntry)
            _persontype.setEnabled(enable)

    def validate_form(self) -> bool:
        """put logic here to check for inconsistent data..
        for example, a begin age should be lower than a lifespan age
        returns True if all fields are valid.
        returns False if one or more fields are False.
        if an invalid field is encountered, display a popup stating the issue.
        """

        for _row in range(self.rowCount() - 1):
            _bage_widget = self.cellWidget(_row, 4)
            _eage_widget = self.cellWidget(_row, 5)

            _begin_age = _bage_widget.get_int()
            _end_age = _eage_widget.get_int()

            if _begin_age is not None and _end_age is not None:
                if _begin_age > _end_age:
                    _bage_widget.set_highlight(True)
                    _eage_widget.set_highlight(True)
                    ShowPopup(
                        self,
                        "Invalid Input",
                        "End Age (%s) must be greater than Begin Age (%s)"
                        % (_end_age, _begin_age),
                    )
                    return False

        return True

    def clear(self):
        self.setRowCount(0)
        self.setHeader()

    def clear_form(self):
        self.clear()


class ExpenseSourceTableWidget(IncomeSourceTableWidget):
    def __init__(self, parent):
        super(ExpenseSourceTableWidget, self).__init__(parent)


class TransferSourceTableWidget(DeleteRowTableWidget):
    def __init__(self, parent):
        super(TransferSourceTableWidget, self).__init__(parent)

        self.setHeader()  # we don't count the "Remove Row" column

        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 125)
        self.setColumnWidth(2, 125)
        # self.setColumnWidth(3, 100)   #Annual Amount
        self.setColumnWidth(4, 75)
        self.setColumnWidth(5, 100)  # Person

        self.setColumnWidth(6, 75)
        self.setColumnWidth(7, 75)

        self.setColumnWidth(8, 50)  # resize remove row

        self._person_enabled: bool = (
            False  # enable/disable PersonTypeEntry (ie, combobox)
        )

    def setHeader(
        self,
    ):  # have to do this since setRowColumn (and clear) remove the headers...
        _header = [
            "Transfer Name",
            "Source Account",
            "Target Account",
            "Annual Amount",
            "Annual\nPercent\nIncrease",
            "Person",
            "Begin Age",
            "End Age",
        ]
        super().setHeader(_header)  # we don't count the "Remove Row" column

    def addRow(self, data=[]):
        _row = self.rowCount()

        assert len(data) in (0, self.numColumns)

        # print("insertRow:", _row)
        self.insertRow(_row)

        # _accounts = ["Client Trad IRA", "Client Roth IRA"]
        # fix me..
        # if self.BasicInfoTab.client_is_married():
        # _accounts += ["Spouse Trad IRA", "Spouse Roth IRA"]

        # _accounts += ["Regular Taxable"]

        # put Select Box here for Source Account
        _src_acct = AccountEntry(parent=self, name="Source Account")
        # _src_acct = QComboBox()
        # _src_acct.addItems(_accounts)
        # self.gridLayout.addWidget(_src_acct, _len, 1)

        # put Select Box here for Target Account
        _tgt_acct = AccountEntry(parent=self, name="Target Account")
        # _tgt_acct = QComboBox()
        # _tgt_acct.addItems(_accounts)
        # self.gridLayout.addWidget(_tgt_acct, _len, 2)

        _descr = StringEntryCell(parent=self, name="Description")
        _amount = MoneyEntryCell(parent=self, name="Annual Amount")
        _cola = PercentEntryCell(parent=self, name="COLA")
        _person = PersonTypeEntry(parent=self)
        _person.setEnabled(self._person_enabled)
        _begin_age = AgeEntryCell(parent=self, name="Begin Age")
        _end_age = AgeEntryCell(parent=self, name="End Age")

        # add any dependencies
        _descr.add_dependencies([_amount])
        _amount.add_dependencies([_descr])
        _cola.add_dependencies([_descr, _amount])
        _begin_age.add_dependencies([_descr, _amount])
        _end_age.add_dependencies([_descr, _amount])

        # add widgets to the row
        self.setCellWidget(_row, 0, _descr)
        self.setCellWidget(_row, 1, _src_acct)
        self.setCellWidget(_row, 2, _tgt_acct)
        self.setCellWidget(_row, 3, _amount)
        self.setCellWidget(_row, 4, _cola)
        self.setCellWidget(_row, 5, _person)
        self.setCellWidget(_row, 6, _begin_age)
        self.setCellWidget(_row, 7, _end_age)

        # add data to the table row if we have data
        # add remove row button to the last column
        self._addRow(_row, data)

    def setEnabledOwner(self, enable: bool) -> None:
        self._person_enabled = enable
        for _row in range(self.rowCount()):
            _persontype = self.cellWidget(_row, 5)
            assert isinstance(_persontype, PersonTypeEntry)
            _persontype.setEnabled(enable)

    def validate_form(self) -> bool:
        """put logic here to check for inconsistent data..
        for example, a begin age should be lower than a lifespan age
        """

        for _row in range(self.rowCount() - 1):
            _src_widget = self.WidgetCell(_row, 1)
            _tgt_widget = self.WidgetCell(_row, 2)

            _src = _src_widget.get()
            _tgt = _tgt_widget.get()

            if _src == _tgt:
                ShowPopup(
                    self,
                    "Invalid Input",
                    "Source and target accounts cannot be the same (%s)" % (_src),
                )

                return False

        for _row in range(self.rowCount() - 1):
            _bage_widget = self.WidgetCell(_row, 6)
            _eage_widget = self.WidgetCell(_row, 7)

            _begin_age = _bage_widget.get_int()
            _end_age = _eage_widget.get_int()

            if _begin_age is not None and _end_age is not None:
                if _begin_age > _end_age:
                    _bage_widget.set_highlight(True)
                    _eage_widget.set_highlight(True)
                    ShowPopup(
                        self,
                        "Invalid Input",
                        "End Age (%s) must be greater than Begin Age (%s)"
                        % (_end_age, _begin_age),
                    )
                    return False

        return True

    def clear(self):
        self.setRowCount(0)
        self.setHeader()

    def clear_form(self):
        self.clear()
