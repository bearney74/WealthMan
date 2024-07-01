import csv

from PyQt6.QtWidgets import (
    QFileDialog,
    QWidget,
    QTableWidget,
    QToolBar,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
    QStyledItemDelegate,
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QAction, QIcon

import logging

logger = logging.getLogger(__name__)


class InitialDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.nDecimals = decimals

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = (
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        text = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if text is None:
            option.text = ""
        elif "%" in text:
            option.text = text
        else:
            try:
                if "." in text:
                    number = float(text)
                    option.text = f"{number:.1f}%"
                else:
                    number = int(text)
                    if number < 0:
                        option.text = f"(${number:,d})"
                    else:
                        option.text = f"${number:,d}"
            except Exception as e:
                logger.error(e)
                print(e)
                option.text = text


class DataTableTab(QWidget):
    def __init__(self, parent=None):
        super(DataTableTab, self).__init__(parent)

        self.parent = parent

        self.table = QTableWidget()
        self.table.setItemDelegate(InitialDelegate(self.table))
        self.table.setItemDelegateForColumn(0, QStyledItemDelegate(self.table))
        self.table.setItemDelegateForColumn(1, QStyledItemDelegate(self.table))
        
        _toolbar = QToolBar("DataTable Toolbar")
        _toolbar.addAction(self.get_csv_action())
        
        layout = QVBoxLayout()
        layout.addWidget(_toolbar)
        layout.addWidget(self.table)
        self.setLayout(layout)

    # Create table
    def createTable(self):
        _header, _vheader, _data = self.parent.tableData.get_data_sheet()

        self.table.hide()
        self.table.clear()
        self.table.setRowCount(len(_data))
        self.table.setColumnCount(len(_data[0]))

        # print("populating table")
        _i = 0
        for _row in _data:
            _j = 0
            for _col in _row:
                if isinstance(_col, (float, int)):
                    _col = str(_col)
                    _value = QTableWidgetItem(_col)
                    if _col.strip().startswith("-"):
                        _value.setForeground(QBrush(QColor(255, 0, 0)))
                    self.table.setItem(_i, _j, _value)
                else:
                    self.table.setItem(_i, _j, QTableWidgetItem(_col))
                _j += 1
            _i += 1
        # print("done populating table")

        # have to put data in table before setting the header, (or header won't display)
        self.table.setHorizontalHeaderLabels(_header)
        self.table.setVerticalHeaderLabels(_vheader)
        # Table will fit the screen horizontally
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.show()

    def get_csv_action(self):
        _action = QAction("Download CSV", self)
        _action.setIcon(QIcon("resources/csv.png"))
        _action.setStatusTip("Download CSV")
        _action.triggered.connect(lambda x: self.get_csv())
        return _action

    def get_csv(self):
        _fname, _x = QFileDialog.getSaveFileName(self.parent, "Save CSV File")
        logger.debug("save csv file, filename:%s" % _fname)
        self.to_csv(_fname)

    def to_csv(self, filename):
        _columns = range(self.table.columnCount())
        _header = [
            self.table.horizontalHeaderItem(column).text() for column in _columns
        ]

        with open(filename, "w") as _fp:
            _csv = csv.writer(_fp, dialect="excel", lineterminator="\n")
            _csv.writerow(_header)
            for _row in range(self.table.rowCount()):
                _csv.writerow(
                    [self.table.item(_row, _column).text() for _column in _columns]
                )
