import unittest

# from PyQt6.QtWidgets import QApplication

from libs.EnumTypes import RelationStatus
from main import Main

from tests.TestCaseQt import TestCaseQt


class FillFormClearForm(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)
        # self.app = QApplication.instance() or QApplication(sys.argv)
        # self.app.processEvents()
        self.form = Main()
        self.BasicInfoTab = self.form.InputsTab.BasicInfoTab
        self.AssetInfoTab = self.form.InputsTab.AssetInfoTab
        self.IncomeInfoTab = self.form.InputsTab.IncomeInfoTab
        self.GlobalVariablesTab = self.form.InputsTab.GlobalVariablesTab

    def tearDown(self):
        TestCaseQt.tearDown(self)
        self.qapp.processEvents()
        self.qapp.exit()
        # del self.qapp

    def test_BasicInfoTab_client(self):
        _client = self.BasicInfoTab._clientinfo
        _spouse = self.BasicInfoTab._spouseinfo

        _status = self.BasicInfoTab._clientinfo._status

        _client._name.setText("Hairy Johnson")
        self.assertEqual(_client._name.text(), "Hairy Johnson")

        _client._name.setText("")
        self.assertEqual(_client._name.text(), "")

        # self.assertEqual(_client._birthDate.setDate())

        _client._retirement_age.setText("69")
        self.assertEqual(_client._retirement_age.text(), "69")
        self.assertEqual(_client._retirement_age.get_int(), 69)

        _client._retirement_age.setText("")
        self.assertEqual(_client._retirement_age.text(), "")
        self.assertEqual(_client._retirement_age.get_int(), None)

        _client._lifespan_age.setText("69")
        self.assertEqual(_client._lifespan_age.text(), "69")
        self.assertEqual(_client._lifespan_age.get_int(), 69)

        _client._lifespan_age.setText("")
        self.assertEqual(_client._lifespan_age.text(), "")
        self.assertEqual(_client._lifespan_age.get_int(), None)

        self.assertEqual(RelationStatus[_status.currentText()], RelationStatus.Single)

        _status.setCurrentText(RelationStatus.Married.name)
        self.assertEqual(RelationStatus[_status.currentText()], RelationStatus.Married)

    def test_BasicInfoTab_spouse(self):
        _spouse = self.BasicInfoTab._spouseinfo

        _spouse._name.setText("Hairy Johnson")
        self.assertEqual(_spouse._name.text(), "Hairy Johnson")

        _spouse._name.setText("")
        self.assertEqual(_spouse._name.text(), "")

        # self.assertEqual(_client._birthDate.setDate())

        _spouse._retirement_age.setText("69")
        self.assertEqual(_spouse._retirement_age.text(), "69")
        self.assertEqual(_spouse._retirement_age.get_int(), 69)

        _spouse._retirement_age.setText("")
        self.assertEqual(_spouse._retirement_age.text(), "")
        self.assertEqual(_spouse._retirement_age.get_int(), None)

        _spouse._lifespan_age.setText("69")
        self.assertEqual(_spouse._lifespan_age.text(), "69")
        self.assertEqual(_spouse._lifespan_age.get_int(), 69)

        _spouse._lifespan_age.setText("")
        self.assertEqual(_spouse._lifespan_age.text(), "")
        self.assertEqual(_spouse._lifespan_age.get_int(), None)

    def test_IncomeTab_SocialSecurity(self):
        _clientSS = self.IncomeInfoTab.clientSS

        for _widget in (self.IncomeInfoTab.clientSS, self.IncomeInfoTab.spouseSS):
            _widget.Amount.setText("1234")
            self.assertEqual(_widget.Amount.text(), "1234")
            self.assertEqual(_widget.Amount.get_int(), 1234)

            _widget.Amount.setText("")
            self.assertEqual(_widget.Amount.text(), "")
            self.assertEqual(_widget.Amount.get_int(), None)

            _widget.Cola.setText("6.9")
            self.assertEqual(_widget.Cola.text(), "6.9")
            self.assertEqual(_widget.Cola.get_float(), 6.9)

            _widget.Cola.setText("")
            self.assertEqual(_widget.Cola.text(), "")
            self.assertEqual(_widget.Cola.get_float(), None)

            _widget.BeginAge.setText("69")
            self.assertEqual(_widget.BeginAge.text(), "69")
            self.assertEqual(_widget.BeginAge.get_int(), 69)

            _widget.BeginAge.setText("")
            self.assertEqual(_widget.BeginAge.text(), "")
            self.assertEqual(_widget.BeginAge.get_int(), None)

        # pension data....
        _incometab = self.IncomeInfoTab
        self.assertEqual(_incometab.pension1Owner.currentText(), "Client")

        _incometab.pension1Amount.setText("1234")
        self.assertEqual(_incometab.pension1Amount.text(), "1234")
        self.assertEqual(_incometab.pension1Amount.get_int(), 1234)

        _incometab.pension1Amount.setText("")
        self.assertEqual(_incometab.pension1Amount.text(), "")
        self.assertEqual(_incometab.pension1Amount.get_int(), None)

        _incometab.pension1Cola.setText("1.2")
        self.assertEqual(_incometab.pension1Cola.text(), "1.2")
        self.assertEqual(_incometab.pension1Cola.get_float(), 1.2)

        _incometab.pension1Cola.setText("")
        self.assertEqual(_incometab.pension1Cola.text(), "")
        self.assertEqual(_incometab.pension1Cola.get_float(), None)

        _incometab.pension1SurvivorBenefits.setText("50.0")
        self.assertEqual(_incometab.pension1SurvivorBenefits.text(), "50.0")
        self.assertEqual(_incometab.pension1SurvivorBenefits.get_float(), 50.0)

        _incometab.pension1SurvivorBenefits.setText("")
        self.assertEqual(_incometab.pension1SurvivorBenefits.text(), "")
        self.assertEqual(_incometab.pension1SurvivorBenefits.get_float(), None)

        _incometab.pension1BeginAge.setText("60")
        self.assertEqual(_incometab.pension1BeginAge.text(), "60")
        self.assertEqual(_incometab.pension1BeginAge.get_int(), 60)

        _incometab.pension1BeginAge.setText("")
        self.assertEqual(_incometab.pension1BeginAge.text(), "")
        self.assertEqual(_incometab.pension1BeginAge.get_int(), None)

        _incometab.pension1EndAge.setText("60")
        self.assertEqual(_incometab.pension1EndAge.text(), "60")
        self.assertEqual(_incometab.pension1EndAge.get_int(), 60)

        _incometab.pension1EndAge.setText("")
        self.assertEqual(_incometab.pension1EndAge.text(), "")
        self.assertEqual(_incometab.pension1EndAge.get_int(), None)

        # pension 2

        _incometab.pension2Amount.setText("1234")
        self.assertEqual(_incometab.pension2Amount.text(), "1234")
        self.assertEqual(_incometab.pension2Amount.get_int(), 1234)

        _incometab.pension2Amount.setText("")
        self.assertEqual(_incometab.pension2Amount.text(), "")
        self.assertEqual(_incometab.pension2Amount.get_int(), None)

        _incometab.pension2Cola.setText("1.2")
        self.assertEqual(_incometab.pension2Cola.text(), "1.2")
        self.assertEqual(_incometab.pension2Cola.get_float(), 1.2)

        _incometab.pension2Cola.setText("")
        self.assertEqual(_incometab.pension2Cola.text(), "")
        self.assertEqual(_incometab.pension2Cola.get_float(), None)

        _incometab.pension2SurvivorBenefits.setText("50.0")
        self.assertEqual(_incometab.pension2SurvivorBenefits.text(), "50.0")
        self.assertEqual(_incometab.pension2SurvivorBenefits.get_float(), 50.0)

        _incometab.pension2SurvivorBenefits.setText("")
        self.assertEqual(_incometab.pension2SurvivorBenefits.text(), "")
        self.assertEqual(_incometab.pension2SurvivorBenefits.get_float(), None)

        _incometab.pension2BeginAge.setText("60")
        self.assertEqual(_incometab.pension2BeginAge.text(), "60")
        self.assertEqual(_incometab.pension2BeginAge.get_int(), 60)

        _incometab.pension2BeginAge.setText("")
        self.assertEqual(_incometab.pension2BeginAge.text(), "")
        self.assertEqual(_incometab.pension2BeginAge.get_int(), None)

        _incometab.pension2EndAge.setText("60")
        self.assertEqual(_incometab.pension2EndAge.text(), "60")
        self.assertEqual(_incometab.pension2EndAge.get_int(), 60)

        _incometab.pension2EndAge.setText("")
        self.assertEqual(_incometab.pension2EndAge.text(), "")
        self.assertEqual(_incometab.pension2EndAge.get_int(), None)

        self.assertEqual(_incometab.gridLayout.count(), 0)


if __name__ == "__main__":
    unittest.main()
