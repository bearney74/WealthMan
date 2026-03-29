import unittest

import sys

sys.path.append("src")

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt, QPoint

from PyQt6.QtTest import QTest

from libs.gui.guihelpers.CustomTableWidgets import IncomeSourceTableWidget
from tests.TestCaseQt import TestCaseQt


class MyTestApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Table will fit the screen horizontally
        self.table = IncomeSourceTableWidget(parent=self)  # QGridLayout()

        self.table.addRow(["Work PT", 12000, 0.0, "Spouse", 51, 52])
        self.setCentralWidget(self.table)
        self.setGeometry(0, 0, 800, 400)

        # print(self.table.getData())


class TestCustomTableWidgets(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)

        self.form = MyTestApp()

    def tearDown(self):
        TestCaseQt.tearDown(self)
        self.qapp.exit()

    def test_all(self):
        self._test_initial()
        self._test_getData_initial()
        self._test_addRow()

    def _test_initial(self):
        self.assertEqual(6, self.form.table.numColumns)
        self.assertEqual(7, self.form.table.columnCount())  # header + "remove row"

        self.assertEqual(1, self.form.table.rowCount())

    def _test_getData_initial(self):
        _data = self.form.table.getData()
        self.assertEqual(1, len(_data))
        self.assertEqual(6, len(_data[0]))

        for _i, _element in enumerate(["Work PT", 12000, 0.0, "Spouse", 51, 52]):
            self.assertEqual(_element, _data[0][_i])

    def _test_addRow(self):
        self.form.table.addRow(["MyTest", 5000, 1.0, "Client", None, None])

        _data = self.form.table.getData()
        self.assertEqual(2, len(_data))
        self.assertEqual(6, len(_data[0]))
        self.assertEqual(6, len(_data[1]))

        for _i, _element in enumerate(["Work PT", 12000, 0.0, "Spouse", 51, 52]):
            self.assertEqual(_element, _data[0][_i])

        for _i, _element in enumerate(["MyTest", 5000, 1.0, "Client"]):
            self.assertEqual(_element, _data[1][_i])

        self.assertIsNone(_data[1][4])
        self.assertIsNone(_data[1][5])

    def _test_focus(self):
        # create tests that use QTest.mouseClick to click on cells, etc to see that
        # new rows are added if we put data in at least one cell in the last row
        pass

        def get_cell_pos(row, col):
            _item = self.form.table.cellWidget(row, col)
            print(_item)
            _global_pos = _item.mapToGlobal(QPoint(0, 0))
            return self.form.table.viewport().mapFromGlobal(_global_pos)

        self.assertEqual(self.form.table.rowCount(), 1)

        # Work PT is located at 0,0
        # _item=self.form.table.cellWidget(0,0)
        # print(_item)
        # _global_pos=_item.mapToGlobal(QPoint(0,0))
        # _pos=self.form.table.viewport().mapFromGlobal(_global_pos)
        _pos = get_cell_pos(0, 0)
        print(_pos.x(), _pos.y())
        QTest.mouseClick(
            self.form.table.viewport(), Qt.MouseButton.LeftButton, pos=_pos
        )

        _pos = get_cell_pos(0, 1)  # self.form.table.item(0,1)
        print(_pos.x(), _pos.y())
        QTest.mouseClick(
            self.form.table.viewport(), Qt.MouseButton.LeftButton, pos=_pos
        )

        # print(_item)

        # an extra row should show up after the focusOut
        self.assertEqual(self.form.table.rowCount(), 2)


if __name__ == "__main__":
    unittest.main()
