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
        _clientSS=self.IncomeInfoTab.clientSS
        
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
        

if __name__ == "__main__":
    unittest.main()
