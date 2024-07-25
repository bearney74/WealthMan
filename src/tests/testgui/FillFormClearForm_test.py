import unittest

from libs.EnumTypes import RelationStatus
from main import Main
from tests.TestCaseQt import TestCaseQt


class FillFormClearForm(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)

        self.form = Main()
        self.BasicInfoTab = self.form.InputsTab.BasicInfoTab
        self.AssetInfoTab = self.form.InputsTab.AssetInfoTab
        self.IncomeInfoTab = self.form.InputsTab.IncomeInfoTab
        self.GlobalVariablesTab = self.form.InputsTab.GlobalVariablesTab

    def tearDown(self):
        TestCaseQt.tearDown(self)

    def _testString(self, variable, s):
        variable.setText(s)
        self.assertEqual(variable.text(), s)

    def _testAge(self, variable, age):
        variable.setText(age)
        self.assertEqual(variable.text(), age)

        if age == "":
            self.assertIsNone(variable.get_int())
        else:
            self.assertEqual(variable.get_int(), int(age))

    def _testMoney(self, variable, amount):
        variable.setText(amount)
        self.assertEqual(variable.text(), amount)

        if amount == "":
            self.assertIsNone(variable.get_int())
        else:
            self.assertEqual(variable.get_int(), int(amount))

    def _testPercent(self, variable, pct):
        variable.setText(pct)
        self.assertEqual(variable.text(), pct)

        if pct == "":
            self.assertIsNone(variable.get_float())
        else:
            self.assertEqual(variable.get_float(), float(pct))

    def _testCheckBox(self, variable, value):
        assert isinstance(value, bool)
        variable.setChecked(value)
        self.assertEqual(variable.isChecked(), value)

    def test_BasicInfoTab_client(self):
        _client = self.BasicInfoTab._clientinfo
        _spouse = self.BasicInfoTab._spouseinfo

        _status = self.BasicInfoTab._clientinfo._status

        self._testString(_client._name, "Hairy Johnson")
        self._testString(_client._name, "")

        self._testAge(_client._retirement_age, "69")
        self._testAge(_client._retirement_age, "")

        self._testAge(_client._lifespan_age, "69")
        self._testAge(_client._lifespan_age, "")

        self.assertEqual(RelationStatus[_status.currentText()], RelationStatus.Single)

        _status.setCurrentText(RelationStatus.Married.name)
        self.assertEqual(RelationStatus[_status.currentText()], RelationStatus.Married)

    def test_BasicInfoTab_spouse(self):
        _spouse = self.BasicInfoTab._spouseinfo

        self._testString(_spouse._name, "Hairy Johnson")
        self._testString(_spouse._name, "")

        self._testAge(_spouse._retirement_age, "69")
        self._testAge(_spouse._retirement_age, "")

        self._testAge(_spouse._lifespan_age, "69")
        self._testAge(_spouse._lifespan_age, "")

    def test_IncomeTab_SocialSecurity(self):
        _clientSS = self.IncomeInfoTab.clientSS

        for _widget in (self.IncomeInfoTab.clientSS, self.IncomeInfoTab.spouseSS):
            self._testMoney(_widget.Amount, "1234")
            self._testMoney(_widget.Amount, "")

            self._testPercent(_widget.Cola, "6.9")
            self._testPercent(_widget.Cola, "")

            self._testAge(_widget.BeginAge, "69")
            self._testAge(_widget.BeginAge, "")

        # pension data....
        _incometab = self.IncomeInfoTab
        self.assertEqual(_incometab.pension1Owner.currentText(), "Client")

        self._testMoney(_incometab.pension1Amount, "1234")
        self._testMoney(_incometab.pension1Amount, "")

        self._testPercent(_incometab.pension1Cola, "1.2")
        self._testPercent(_incometab.pension1Cola, "")

        self._testPercent(_incometab.pension1SurvivorBenefits, "50.0")
        self._testPercent(_incometab.pension1SurvivorBenefits, "")

        self._testAge(_incometab.pension1BeginAge, "60")
        self._testAge(_incometab.pension1BeginAge, "")

        self._testAge(_incometab.pension1EndAge, "60")
        self._testAge(_incometab.pension1EndAge, "")

        # pension 2

        self._testMoney(_incometab.pension2Amount, "1234")
        self._testMoney(_incometab.pension2Amount, "")

        self._testPercent(_incometab.pension2Cola, "1.2")
        self._testPercent(_incometab.pension2Cola, "")

        self._testPercent(_incometab.pension2SurvivorBenefits, "50.0")
        self._testPercent(_incometab.pension2SurvivorBenefits, "")

        self._testAge(_incometab.pension2BeginAge, "60")
        self._testAge(_incometab.pension2BeginAge, "")

        self._testAge(_incometab.pension2EndAge, "60")
        self._testAge(_incometab.pension2EndAge, "")

        self.assertEqual(_incometab.gridLayout.count(), 0)

        # need to add income sources...

    def test_GlobalVariablesTab(self):
        _gvt = self.GlobalVariablesTab
        self._testAge(_gvt._forecast_years, "33")
        self._testAge(_gvt._forecast_years, "")

        self._testPercent(_gvt._Inflation, "33")
        self._testPercent(_gvt._Inflation, "")

        self._testCheckBox(_gvt._InTodaysDollars, True)
        self._testCheckBox(_gvt._InTodaysDollars, False)

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

        self._testPercent(_gvt._SurplusAccountInterestRate, "2.9")
        self._testPercent(_gvt._SurplusAccountInterestRate, "")


if __name__ == "__main__":
    unittest.main()
