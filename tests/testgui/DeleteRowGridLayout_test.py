import unittest

import sys

sys.path.append("src")

from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton

# from libs.DataVariables import DataVariables
# from libs.EnumTypes import RelationStatusType, PersonType
from libs.gui.guihelpers.DeleteRowGridLayout import DeleteRowGridLayout
from libs.gui.guihelpers.Entry import Entry

from tests.TestCaseQt import TestCaseQt


class MyTestApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Table will fit the screen horizontally
        self.gridLayout = DeleteRowGridLayout(self)  # QGridLayout()
        self.gridLayout.set_header(
            [
                "A String",
                "An Integer",
                "A Float",
            ]
        )

        container = QWidget()
        container.setLayout(self.gridLayout)
        self.setCentralWidget(container)


class DeleteRowGridLayoutTest(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)

        self.form = MyTestApp()

    def tearDown(self):
        TestCaseQt.tearDown(self)
        self.qapp.exit()

    def test_all(self):
        self._add_row()
        self._delete_row()
        self._delete_row_by_button()

    def _add_row(self):
        _label = QLabel("My String")
        _int = Entry()
        _int.setText("3")
        _float = Entry()
        _float.setText("4.0")

        self.form.gridLayout.add_row([_label, _int, _float])

        self.assertEqual(self.form.gridLayout.rowCount(), 1)

        # _data is a list of lists...
        _data = self.form.gridLayout.get_data()

        self.assertEqual(3, len(_data[0]))
        self.assertEqual(_label.text(), _data[0][0].text())
        self.assertEqual(_int.text(), _data[0][1].text())
        self.assertEqual(_float.text(), _data[0][2].text())

    def _delete_row(self):
        self.form.gridLayout._delete_row(1)
        self.assertEqual(self.form.gridLayout.rowCount(), 0)

    def _delete_row_by_button(self):
        self.assertEqual(self.form.gridLayout.rowCount(), 0)

        _label = QLabel("My String2")
        _int = Entry()
        _int.setText("5")
        _float = Entry()
        _float.setText("6.0")

        # we return a row_id because the underlaying row_id will not necessary match the
        # number of rows in the table if we have deleted several rows
        # (ie, the deleted rows really don't get removed.. only the widgets in them gets removed)
        _row_id = self.form.gridLayout.add_row([_label, _int, _float])

        self.assertEqual(self.form.gridLayout.rowCount(), 1)

        _button = self.form.gridLayout.rowDeleteButton(_row_id)
        self.assertTrue(isinstance(_button, QPushButton))

        _button.click()
        self.assertEqual(self.form.gridLayout.rowCount(), 0)

        _data = self.form.gridLayout.get_data()
        self.assertEqual(0, len(_data))


if __name__ == "__main__":
    unittest.main()
