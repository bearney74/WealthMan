
from PyQt6.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
    QStyledItemDelegate,
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor

#from libs.DataVariables import DataVariables
from libs.TableData import TableData

#from .Projections import Projections

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
                number = int(text)
                if number < 0:
                    option.text = f"(${number:,d})"
                else:
                    option.text = f"${number:,d}"
            except Exception as e:
                logger.error(e)
                print(e)


class DataTableTab(QWidget):
    def __init__(self, parent=None):
        super(DataTableTab, self).__init__(parent)

        self.table = QTableWidget()
        self.table.setItemDelegate(InitialDelegate(self.table))
        self.table.setItemDelegateForColumn(0, QStyledItemDelegate(self.table))
        self.table.setItemDelegateForColumn(1, QStyledItemDelegate(self.table))
        
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    # Create table
    def createTable(self, dt: TableData):
        assert isinstance(dt, TableData)
        #_f = Forecast(dv)
        #datatable = p.execute()
        _header, _data = dt.get_data_sheet()

        self.table.hide()
        self.table.clear()
        self.table.setRowCount(len(_data))
        self.table.setColumnCount(len(_data[0]))

        # print("populating table")
        _i = 0
        for _row in _data:
            _j = 0
            for _col in _row:
                # print(_i, _j, _col)
                _value = QTableWidgetItem(_col)
                if _col.strip().startswith("-"):
                    _value.setForeground(QBrush(QColor(255, 0, 0)))
                self.table.setItem(_i, _j, _value)
                _j += 1
            _i += 1
        # print("done populating table")

        # have to put data in table before setting the header, (or header won't display)
        self.table.setHorizontalHeaderLabels(_header)
        # Table will fit the screen horizontally
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.show()
