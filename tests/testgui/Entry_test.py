import unittest
import sys

sys.path.append("src")

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtTest import QTest

from libs.gui.guihelpers.Entry import YearEntry

from tests.TestCaseQt import TestCaseQt


class MyTestApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Table will fit the screen horizontally
        _layout = QVBoxLayout()

        # put entry widgets here to test..
        self._year = YearEntry()

        _layout.addWidget(self._year)

        container = QWidget()
        container.setLayout(_layout)
        self.setCentralWidget(container)


class EntryTest(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)

        self.form = MyTestApp()

    def tearDown(self):
        TestCaseQt.tearDown(self)
        self.qapp.exit()

    def test_entry(self):
        self._test_year()

    def _test_year(self):
        _year = self.form._year

        QTest.keyClicks(_year, "2000")
        # _year.setText("2000")
        self.assertEqual(_year.get_int(), 2000)

        # now try some invalid years (valid years are 1920 - 2099)
        QTest.keyClicks(_year, "1900")
        self.assertEqual(
            _year.get_int(), 2000
        )  # 1900 is ignored.. the old value is put back in..

        QTest.keyClicks(_year, "2100")
        self.assertEqual(
            _year.get_int(), 2000
        )  # 1900 is ignored.. the old value is put back in..

        # with self.assertRaises(ValueError):
        # _year.setText("2100")  # year has to be 1920 - 2099 (by default)


if __name__ == "__main__":
    unittest.main()
