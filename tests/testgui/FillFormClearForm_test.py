import unittest

import sys

sys.path.append("src")

from PyQt6.QtWidgets import QWidgetItem, QPushButton
from PyQt6.QtTest import QTest

from libs.gui.guihelpers.Entry import AgeEntry, MoneyEntry, FloatEntry, StringEntry

from libs.DataVariables import DataVariables
from libs.EnumTypes import RelationStatusType, PersonType
from main import Main

from tests.TestCaseQt import TestCaseQt


class FillFormClearForm(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)

        self.form = Main()

    def tearDown(self):
        TestCaseQt.tearDown(self)
        self.qapp.exit()

    def _testString(self, variable, s):
        assert isinstance(variable, StringEntry)
        variable.clear()
        QTest.keyClicks(variable, s)
        self.assertEqual(variable.text(), s)

    def _testAge(self, variable, age):
        assert isinstance(variable, AgeEntry)

        variable.clear()
        QTest.keyClicks(variable, age)
        self.assertEqual(variable.text(), age)

    def _testMoney(self, variable, amount):
        assert isinstance(variable, MoneyEntry)
        variable.clear()
        QTest.keyClicks(variable, amount)
        self.assertEqual(variable.text(), amount)

        if amount == "":
            self.assertIsNone(variable.get_int())
        else:
            self.assertEqual(variable.get_int(), int(amount))

    def _testPercent(self, variable, pct):
        assert isinstance(variable, FloatEntry)
        variable.clear()
        QTest.keyClicks(variable, pct)
        self.assertEqual(variable.text(), pct)

        if pct == "":
            self.assertIsNone(variable.get_float())
        else:
            self.assertEqual(variable.get_float(), float(pct))

    def _testCheckBox(self, variable, value):
        assert isinstance(value, bool)
        # fix me.. this doesn't appear to click on the button..
        # QTest.mouseClick(variable, Qt.MouseButton.LeftButton)

        variable.setChecked(value)
        self.assertEqual(variable.isChecked(), value)

    def test_tabs(self):
        # just put all the tests under one tab so that we don't open
        # bunch of applications (it appears that each "test function"
        # creates a new instance of the application
        self._test_BasicInfoTab()
        self._test_IncomeTab_SocialSecurity()
        # self._test_ExpenseTab()  planning on replacing this, so just comment it out for now..
        self._test_Assets()
        self._test_Transfers()
        self._test_GlobalVariablesTab()
        self._test_MiscTab()

    def _test_BasicInfoTab(self):
        _bit = self.form.InputsTab.BasicInfoTab

        _client = _bit._clientinfo
        _spouse = _bit._spouseinfo

        _status = _bit._clientinfo._status

        self._testString(_client._name, "Hairy Johnson")
        self._testString(_client._name, "")

        self._testAge(_client._retirement_age, "69")
        self._testAge(_client._retirement_age, "")

        self._testAge(_client._lifespan_age, "69")
        self._testAge(_client._lifespan_age, "")

        self.assertEqual(_status.get(), RelationStatusType.SINGLE)

        _status.set(
            RelationStatusType.MARRIED
        )  # setCurrentText(RelationStatus.Married.name)
        self.assertEqual(_status.get(), RelationStatusType.MARRIED)

        self._testString(_spouse._name, "Hairy Johnson")
        self._testString(_spouse._name, "")

        self._testAge(_spouse._retirement_age, "69")
        self._testAge(_spouse._retirement_age, "")

        self._testAge(_spouse._lifespan_age, "69")
        self._testAge(_spouse._lifespan_age, "")

    def _test_IncomeTab_SocialSecurity(self):
        _incometab = self.form.InputsTab.IncomeInfoTab

        self._testMoney(_incometab.clientSS.Amount, "1234")
        self._testMoney(_incometab.clientSS.Amount, "")

        self._testAge(_incometab.clientSS.BeginAge, "63")
        self._testAge(_incometab.clientSS.BeginAge, "62")
        self._testAge(_incometab.clientSS.BeginAge, "")

        # enable spouse SS form
        _incometab.spouseSS.setEnabled(True)
        self.assertTrue(_incometab.spouseSS.isEnabled())

        self._testMoney(_incometab.spouseSS.Amount, "1234")
        self._testMoney(_incometab.spouseSS.Amount, "")

        self._testAge(_incometab.spouseSS.BeginAge, "63")
        self._testAge(_incometab.spouseSS.BeginAge, "62")
        self._testAge(_incometab.spouseSS.BeginAge, "")

        # pension data....
        self.assertEqual(_incometab.pension1.Owner.currentText(), "Client")

        self._testMoney(_incometab.pension1.Amount, "1234")
        self._testMoney(_incometab.pension1.Amount, "")

        self._testPercent(_incometab.pension1.Cola, "1.2")
        self._testPercent(_incometab.pension1.Cola, "")

        self._testPercent(_incometab.pension1.SurvivorBenefits, "50.0")
        self._testPercent(_incometab.pension1.SurvivorBenefits, "")

        self._testAge(_incometab.pension1.BeginAge, "60")
        self._testAge(_incometab.pension1.BeginAge, "")

        self._testAge(_incometab.pension1.EndAge, "60")
        self._testAge(_incometab.pension1.EndAge, "")

        # pension 2

        self._testMoney(_incometab.pension2.Amount, "1234")
        self._testMoney(_incometab.pension2.Amount, "")

        self._testPercent(_incometab.pension2.Cola, "1.2")
        self._testPercent(_incometab.pension2.Cola, "")

        self._testPercent(_incometab.pension2.SurvivorBenefits, "50.0")
        self._testPercent(_incometab.pension2.SurvivorBenefits, "")

        self._testAge(_incometab.pension2.BeginAge, "60")
        self._testAge(_incometab.pension2.BeginAge, "")

        self._testAge(_incometab.pension2.EndAge, "60")
        self._testAge(_incometab.pension2.EndAge, "")

        # check that we have no extra income sources. (except for the blank row)
        self.assertEqual(_incometab.table.rowCount(), 1)
        _data = _incometab.table.getData()
        self.assertEqual(len(_data), 0)

        # need to add income sources...

    def _test_ExpenseTab(self):
        _expensetab = self.form.InputsTab.ExpenseInfoTab

        self.assertEqual(
            _expensetab.gridLayout.rowCount(), 0
        )  # there is a header row..

        _expensetab._add_expense_button.click()

        self.assertEqual(_expensetab.gridLayout.rowCount(), 1)

        # row #3
        _expensetab._add_row("my data", 123, "", PersonType.CLIENT, 25, 30)
        self.assertEqual(_expensetab.gridLayout.rowCount(), 2)

        dv = DataVariables()
        _expensetab.export_data(dv)

        self.assertEqual(2, len(dv.expenses))
        _rec = dv.expenses[1]

        self.assertEqual("my data", _rec.descr)
        self.assertEqual(123, _rec.amount)
        self.assertIsNone(_rec.COLA)
        self.assertEqual(PersonType.CLIENT, _rec.owner)
        self.assertEqual(25, _rec.begin_age)
        self.assertEqual(30, _rec.end_age)

        # click on a rows delete button to see if it will delete the data..
        _delete_button = _expensetab.gridLayout.itemAtPosition(2, 6)
        assert isinstance(_delete_button, QWidgetItem)
        assert isinstance(_delete_button.widget(), QPushButton)
        # self.assertIsNotNone(_delete_button.widget())
        _delete_button.widget().click()

        dv1 = DataVariables()
        _data1 = _expensetab.export_data(dv1)
        self.assertEqual(1, len(dv1.expenses))

        _expensetab.clear_form()
        dv2 = DataVariables()
        _data1 = _expensetab.export_data(dv2)
        self.assertEqual(1, len(dv1.expenses))  # header should still exist..

    def _test_Assets(self):
        _assettab = self.form.InputsTab.AssetInfoTab
        # todo
        # add some tests for the assets tab

    def _test_Transfers(self):
        _transfertab = self.form.InputsTab.TransferInfoTab
        # todo
        # add some tests for the transfer tab

    def _test_GlobalVariablesTab(self):
        _gvt = self.form.InputsTab.GlobalVariablesTab

        self._testAge(_gvt._forecast_years, "33")
        self._testAge(_gvt._forecast_years, "")

        self._testPercent(_gvt._Inflation, "33")
        self._testPercent(_gvt._Inflation, "")

        self._testPercent(_gvt._ssCola, "33")
        self._testPercent(_gvt._ssCola, "")

        self.assertFalse(_gvt._InTodaysDollars.isChecked())
        self._testCheckBox(_gvt._InTodaysDollars, True)
        self._testCheckBox(_gvt._InTodaysDollars, False)

        self.assertFalse(_gvt._SurplusAccount.isChecked())
        self._testCheckBox(_gvt._SurplusAccount, False)

        # need to click on checkbox for this assert to work
        _gvt._SurplusAccount.click()
        self.assertTrue(_gvt._SurplusAccountInterestRate.isEnabled())
        _gvt._SurplusAccount.click()
        self.assertFalse(_gvt._SurplusAccountInterestRate.isEnabled())

        self._testCheckBox(_gvt._SurplusAccount, True)

        # need to click on checkbox for this assert to work
        _gvt._SurplusAccount.click()
        self.assertFalse(_gvt._SurplusAccountInterestRate.isEnabled())

        _gvt._SurplusAccount.click()
        self._testPercent(_gvt._SurplusAccountInterestRate, "2.9")
        self._testPercent(_gvt._SurplusAccountInterestRate, "")

    def _test_MiscTab(self):
        _misc = self.form.InputsTab.MiscInfoTab

        # test defaults
        self.assertEqual(_misc._ror.get_float(), 11.85)
        self.assertEqual(_misc._ror_stdDev.get_float(), 19.40)

        self.assertEqual(_misc._inflation_rate.get_float(), 3.11)
        self.assertEqual(_misc._inflation_stdDev.get_float(), 3.90)

        self._testPercent(_misc._ror, "9.8")
        self._testPercent(_misc._ror, "")

        self._testPercent(_misc._inflation_rate, "2.5")
        self._testPercent(_misc._inflation_stdDev, "")

        # historial Analysis variables
        self._testPercent(_misc._pctStocks, "85")
        self._testPercent(_misc._pctStocks, "")

        self._testPercent(_misc._pctBonds, "15")
        self._testPercent(_misc._pctBonds, "")


if __name__ == "__main__":
    unittest.main()
