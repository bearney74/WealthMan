from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidgetItem, QStyle
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class DeleteRowGridLayout(QGridLayout):
    def __init__(self, parent):
        super(DeleteRowGridLayout, self).__init__()
        self.parent = parent
        self._number_of_rows = 0

        _pixmapi = QStyle.StandardPixmap.SP_DialogDiscardButton
        self._icon = QIcon(self.parent.style().standardIcon(_pixmapi))
        # self._icon = QIcon(QPixmap(":images/delete.png"))

    def set_header(self, header):
        _col = 0
        for item in header:
            self.addWidget(QLabel(item, wordWrap="\n" in item), 0, _col)
            _col += 1

        # add delete column to header
        self.addWidget(QLabel("Delete"), 0, _col)

    def add_row(self, data) -> int:
        self._number_of_rows += 1
        for _i, _item in enumerate(data):
            self.addWidget(_item, self._number_of_rows, _i)

        _button = QPushButton()
        _button.clicked.connect(
            lambda checked, row_id=self._number_of_rows: self._delete_row(row_id)
        )
        self.addWidget(_button, self._number_of_rows, len(data))

        # add icon to button
        _button.setIcon(self._icon)
        _button.setIconSize(QSize(32, 32))

        return self._number_of_rows

    def _delete_row(self, row_id):
        for _i in range(0, self.columnCount()):
            _item = self.itemAtPosition(row_id, _i)
            if isinstance(_item, QWidgetItem):
                self.removeWidget(_item.widget())
            elif _item is not None:
                self.removeItem(_item)  # not sure if this ever gets called
            del _item

    def get_data(self):
        """return all rows that have not been deleted"""
        _data = []
        for _i in range(1, super().rowCount()):  # start with 1 to skip header row.
            _delete_flag, _row_data = self._get_row_data(_i)
            if not _delete_flag:  # this row was not deleted..
                _data.append(_row_data)

        return _data

    def rowCount(self):
        _valid_rows = 0
        for _i in range(1, super().rowCount()):  # start with 1 to skip header row.
            _delete_flag, _row_data = self._get_row_data(_i)
            if not _delete_flag:  # this row was not deleted..
                _valid_rows += 1

        return _valid_rows

    def rowDeleteButton(self, row_id):
        _item = self.itemAtPosition(row_id, self.columnCount() - 1)

        assert isinstance(_item, QWidgetItem)
        assert isinstance(_item.widget(), QPushButton)

        return _item.widget()

    def _get_row_data(self, row_id):
        _data = []
        _flag = True  # used to see if this row was deleted or not..
        for _j in range(
            self.columnCount() - 1
        ):  # -1 because we don't want the delete Button in the last column
            _item = self.itemAtPosition(row_id, _j)
            if (
                _flag and _item is not None
            ):  # we have a valid item, so this row contains data
                _flag = False
            if _item is not None:
                _data.append(_item.widget())

        return _flag, _data

    def clear(self):
        # header row is at 0, (so start deleting at row 1)
        for _i in range(1, super().rowCount()):
            self._delete_row(_i)
