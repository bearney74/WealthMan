from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize

from libs.resources import qt_assets

# make ruff happy..
dir(qt_assets)


class DeleteRowGridLayout(QGridLayout):
    def __init__(self):
        super(DeleteRowGridLayout, self).__init__()
        self._number_of_rows = 0

        self._icon = QIcon(QPixmap(":images/delete.png"))

    def set_header(self, header):
        _col = 0
        for item in header:
            if "\n" in item:
                _label = QLabel(item, wordWrap=True)
            else:
                _label = QLabel(item)

            self.addWidget(_label, 0, _col)
            _col += 1

        # add delete column to header
        self.addWidget(QLabel("Delete"), 0, _col)

    def add_row(self, data):
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

    def _delete_row(self, row_id):
        for _i in range(0, self.columnCount()):
            _item = self.itemAtPosition(row_id, _i)
            self.removeWidget(_item.widget())
            # self.removeItem(_item)
            del _item

    def get_data(self):
        """return all rows that have not been deleted"""
        _data = []
        for _i in range(1, self.rowCount()):  # start with 1 to skip header row.
            _delete_flag, _row_data = self._get_row_data(_i)
            if not _delete_flag:  # this row was not deleted..
                _data.append(_row_data)

        return _data

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
        for _i in range(1, self.rowCount()):
            self._delete_row(_i)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
    from PyQt6.QtCore import Qt

    class MainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("QGridLayout Example")

            _layout = QVBoxLayout()
            _layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            grid = DeleteRowGridLayout()
            grid.set_header(["Name", "Item", "Edit"])

            # Adding widgets to specific (row, column)
            for _i in range(0, 5):
                grid.add_row(
                    [QLabel("my name %s" % _i), QLabel("my Item %s" % _i), QLineEdit()]
                )

            _layout.addLayout(grid)
            self.setLayout(_layout)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
