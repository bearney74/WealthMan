import unittest

import sys

sys.path.append("src")

from PyQt6.QtWidgets import QMainWindow, QWidget

# from libs.DataVariables import DataVariables
# from libs.EnumTypes import RelationStatusType, PersonType
from libs.gui.guihelpers.DeleteRowGridLayout import DeleteRowGridLayout

from tests.TestCaseQt import TestCaseQt


class MyTestApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Table will fit the screen horizontally
        self.gridLayout = DeleteRowGridLayout()  # QGridLayout()
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
        # _hlayout = QHBoxLayout()
        # _hlayout.addLayout(self.gridLayout)
        # self.setLayout(self.gridLayout)
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

    def test_add_row(self):
        pass


# todo add tests here to test out


if __name__ == "__main__":
    unittest.main()
