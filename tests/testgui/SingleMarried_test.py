import unittest

from libs.EnumTypes import RelationStatus
from main import Main

from tests.TestCaseQt import TestCaseQt
# app = QApplication(sys.argv)


class SingleMarried(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)

        # self.app=QApplication.instance() or QApplication(sys.argv) #QApplication(["--platform offscreen"])
        # self.app=QApplication(sys.argv)
        # self.app.processEvents()
        self.form = Main()
        self.BasicInfoTab = self.form.InputsTab.BasicInfoTab
        self.AssetInfoTab = self.form.InputsTab.AssetInfoTab
        self.IncomeInfoTab = self.form.InputsTab.IncomeInfoTab
        self.GlobalVariablesTab = self.form.InputsTab.GlobalVariablesTab

    def tearDown(self):
        TestCaseQt.tearDown(self)
        # self.app.processEvents()
        self.qapp.exit()
        # del self.qapp

    def test_main(self):
        _status = self.BasicInfoTab._clientinfo._status

        self.assertEqual(RelationStatus[_status.currentText()], RelationStatus.Single)

        # make sure that spouse widgets are disabled since We choose single
        self.form.InputsTab.tabs.setCurrentIndex(0)  # select Basic Tab
        self.assertFalse(self.BasicInfoTab._spouseinfo.isEnabled())
        self.form.InputsTab.tabs.setCurrentIndex(3)  # select Basic Tab
        self.assertFalse(self.AssetInfoTab._spouseinfo.isEnabled())

        # check IncomeInfo Tab
        self.form.InputsTab.tabs.setCurrentIndex(1)  # select Income Tab..
        self.assertFalse(self.IncomeInfoTab.spouseSS.isEnabled())
        self.assertFalse(self.IncomeInfoTab.pension1OwnerLabel.isEnabled())
        self.assertFalse(self.IncomeInfoTab.pension1Owner.isEnabled())
        self.assertFalse(self.IncomeInfoTab.pension2OwnerLabel.isEnabled())
        self.assertFalse(self.IncomeInfoTab.pension2Owner.isEnabled())

        self.form.InputsTab.tabs.setCurrentIndex(4)  # select Global tab
        self.assertFalse(self.GlobalVariablesTab._FilingStatusOnceWidowed.isEnabled())

        # change status to Married...
        _status.setCurrentText(RelationStatus.Married.name)
        self.assertEqual(RelationStatus[_status.currentText()], RelationStatus.Married)

        # make sure that spouse widgets are enabled since We choose married
        self.form.InputsTab.tabs.setCurrentIndex(0)  # select Basic Tab
        self.assertTrue(self.BasicInfoTab._spouseinfo.isEnabled())

        self.form.InputsTab.tabs.setCurrentIndex(3)  # select Asset
        self.assertTrue(self.AssetInfoTab._spouseinfo.isEnabled())

        self.form.InputsTab.tabs.setCurrentIndex(1)  # select Income Tab..
        self.assertTrue(self.IncomeInfoTab.spouseSS.isEnabled())
        self.assertTrue(self.IncomeInfoTab.pension1OwnerLabel.isEnabled())
        self.assertTrue(self.IncomeInfoTab.pension1Owner.isEnabled())
        self.assertTrue(self.IncomeInfoTab.pension2OwnerLabel.isEnabled())
        self.assertTrue(self.IncomeInfoTab.pension2Owner.isEnabled())

        self.form.InputsTab.tabs.setCurrentIndex(4)  # select Global tab
        self.assertTrue(self.GlobalVariablesTab._FilingStatusOnceWidowed.isEnabled())


if __name__ == "__main__":
    unittest.main()
