from PyQt6.QtWidgets import QComboBox, QTableWidget, QPushButton, QStyle
from PyQt6.QtGui import QDoubleValidator, QIcon
from PyQt6.QtCore import Qt, QSize

from enum import Enum

import sys

sys.path.append("../../src")

from libs.gui.guihelpers.Entry import (
    Entry,
    StringEntry,
    FloatEntry,
    IntegerEntry,
    MoneyEntry,
    EnumEntry,
)


class AgeEntryCell(IntegerEntry):
    def __init__(
        self,
        name: str = None,
        parent=None,
        min: int = 0,
        max: int = 99,
        required: bool = False,
    ):
        super(AgeEntryCell, self).__init__(
            name=name, parent=parent, min=min, max=max, required=required
        )
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

        assert isinstance(parent, QTableWidget)
        self.parent = parent

    def focusInEvent(
        self, event
    ):  # need to override inherited focusInEvent, and let TableWidget handle the highlighting
        pass

    def focusOutEvent(self, event):
        super().focusOutEvent(event)

        self.parent.addRowCheck(not self.isEmpty())
        self.parent.focusOutEvent(event)


class MoneyEntryCell(MoneyEntry):
    def __init__(
        self, name: str = None, parent=None, min: int = 0, required: bool = False
    ):
        super(MoneyEntryCell, self).__init__(
            name=name, parent=parent, min=min, limit_size=None, required=required
        )
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

        assert isinstance(parent, QTableWidget)
        self.parent = parent

    def focusInEvent(
        self, event
    ):  # need to override inherited focusInEvent, and let TableWidget handle the highlighting
        pass

    def focusOutEvent(self, event):
        super().focusOutEvent(event)

        self.parent.addRowCheck(not self.isEmpty())
        self.parent.focusOutEvent(event)


class PercentEntryCell(FloatEntry):
    def __init__(
        self,
        name: str = None,
        parent=None,
        min: int = 0.0,
        max: int = 9.9,
        num_decimal_places: int = 1,
        required: bool = False,
    ):
        super(PercentEntryCell, self).__init__(
            name=name,
            parent=parent,
            min=min,
            max=max,
            num_decimal_places=num_decimal_places,
            required=required,
        )

        _dv = QDoubleValidator(min, max, num_decimal_places)
        _dv.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.setValidator(_dv)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

        assert isinstance(parent, QTableWidget)
        self.parent = parent

    def focusInEvent(
        self, event
    ):  # need to override inherited focusInEvent, and let TableWidget handle the highlighting
        pass

    def focusOutEvent(self, event):
        super().focusOutEvent(event)

        self.parent.addRowCheck(not self.isEmpty())
        self.parent.focusOutEvent(event)


class StringEntryCell(StringEntry):
    def __init__(self, parent=None, name: str = None):
        super(StringEntryCell, self).__init__(parent=parent, name=name)
        self.parent = parent

    def focusOutEvent(self, event):
        print("StringEntryCell:focusOutEvent")
        super().focusOutEvent(event)

        self.parent.addRowCheck(not self.isEmpty())
        self.parent.focusOutEvent(event)


class DeleteRowTableWidget(QTableWidget):
    def __init__(self, parent):
        super(DeleteRowTableWidget, self).__init__(parent)  # start with 2 rows
        assert parent is not None
        self.parent = parent

        _pixmapi = QStyle.StandardPixmap.SP_DialogDiscardButton
        self._trashcan_icon = QIcon(self.parent.style().standardIcon(_pixmapi))

        self._dependencies = []

    def setHeader(self, header):
        # print("setHeader")
        # header=header
        header.append("Remove\nRow")
        self.setColumnCount(len(header))
        self.numColumns = len(header) - 1
        self.setHorizontalHeaderLabels(header)

        assert self.numColumns == self.columnCount() - 1

    def addRow(self, data):  # override this function
        pass

    def validate_form(self):  # override this function to put logic checks here..
        pass

    def addRowCheck(self, contains_data: bool):
        """checks to see if we are on the last row, and adds a new last row if we start adding
        content to the last row.
        """

        # print("addRowCheck")
        # print(self.currentRow(), self.rowCount()-1)
        if contains_data and self.currentRow() == self.rowCount() - 1:
            # print("add row")
            self.addRow()

    def focusOutEvent(self, event):
        """highlights fields that need to be populated.  If certains fields are populated
        other fields need data
        """
        # print("focusOutEvent")
        _list = []
        for _row in range(self.rowCount() - 1):
            # _list=[]
            for _col in range(self.numColumns):
                _item = self.cellWidget(_row, _col)
                if not isinstance(_item, EnumEntry):
                    if not _item.isEmpty():
                        # print("has data:", _item)
                        for _widget in _item._dependencies:
                            if _widget.isEmpty() and _widget not in _list:
                                _list.append(_widget)

        # print(_list)
        for _widget in _list:
            _widget.set_highlight(True)
            # print("highlight:", _widget)
            # else:
            #  _widget.set_highlight(False)
            #  print("no highlight", _widget)

    def _addRow(self, row, data):
        if len(data) == self.numColumns:
            for _col, _element in enumerate(data):
                _item = self.cellWidget(row, _col)
                # print(type(_item), isinstance(_item, EnumEntry))
                if isinstance(_item, Entry):
                    _item.setText(_element)
                    if isinstance(_item, (IntegerEntry, FloatEntry)):
                        _item.setAlignment(Qt.AlignmentFlag.AlignRight)
                elif isinstance(_item, EnumEntry):
                    # print("_addRow", _item)
                    _item.set(_element)
                elif isinstance(_item, QComboBox):
                    _item.setCurrentText(_element)

        # add button to remove this row..
        _button = QPushButton()
        _button = QPushButton()
        _button.clicked.connect(lambda checked, row_id=row: self.removeRow(row_id))
        _button.setIcon(self._trashcan_icon)
        _button.setIconSize(QSize(32, 32))

        self.setCellWidget(row, self.numColumns, _button)

        # add any dependencies

    def removeRow(self, row):
        # print("remove Row", row)
        super().removeRow(row)
        if self.rowCount() < 2:
            self.addRow()

    def getRowData(self, rowID):
        _data = []
        # _type=[]
        for _col in range(self.columnCount()):
            _item = self.cellWidget(rowID, _col)
            if isinstance(_item, IntegerEntry):
                _data.append(_item.get_int())
                # _type.append(IntegerEntry)
            elif isinstance(_item, FloatEntry):
                _data.append(_item.get_float())
                # _type.append(FloatEntry)
            elif isinstance(_item, StringEntry):
                _data.append(_item.text())
                # _type.append(StringEntry)
            elif isinstance(_item, EnumEntry):
                _data.append(_item.get())
                # _type.append(EnumEntry)
            elif isinstance(_item, QComboBox):
                _data.append(_item.currentText())

        # check to see if this row is empty (ie, mostly "" and None, except for EnumEntry, which have
        # a value reguardless.
        _flag = True
        for _pos, _element in enumerate(_data):
            if _element not in (None, ""):
                # print(type(_element), _element)
                if not isinstance(
                    _element, Enum
                ):  # EnumEntry always have a value, so just ignore them.
                    _flag = False

        if not _flag:
            return _data

        return None

    def getData(self):
        _data = []
        for _row in range(self.rowCount()):
            _result = self.getRowData(_row)
            if _result is not None:
                _data.append(_result)

        return _data
