import unittest
import sys

sys.path.append("src")

from libs.EnumTypes import RelationStatusType
from main import Main
from tests.TestCaseQt import TestCaseQt


class SingleMarried(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)

        self.form = Main()

    def tearDown(self):
        TestCaseQt.tearDown(self)
        self.qapp.exit()

    def test_main(self):
        _InputsTab = self.form.InputsTab
        _BasicInfoTab = self.form.InputsTab.BasicInfoTab
        _AssetInfoTab = self.form.InputsTab.AssetInfoTab
        _IncomeInfoTab = self.form.InputsTab.IncomeInfoTab
        _GlobalVariablesTab = self.form.InputsTab.GlobalVariablesTab

        _status = self.form.InputsTab.BasicInfoTab._clientinfo._status

        self.assertEqual(_status.get(), RelationStatusType.SINGLE)

        # make sure that spouse widgets are disabled since We choose single
        _InputsTab.tabs.setCurrentIndex(0)  # select Basic Tab
        self.assertFalse(_BasicInfoTab._spouseinfo.isEnabled())
        _InputsTab.tabs.setCurrentIndex(3)  # select Basic Tab
        self.assertFalse(_AssetInfoTab._spouseinfo.isEnabled())

        # check IncomeInfo Tab
        _InputsTab.tabs.setCurrentIndex(1)  # select Income Tab..
        self.assertFalse(_IncomeInfoTab.spouseSS.isEnabled())
        # self.assertFalse(_IncomeInfoTab.pension1.OwnerLabel.isEnabled())
        # self.assertFalse(_IncomeInfoTab.pension1.Owner.isEnabled())
        # self.assertFalse(_IncomeInfoTab.pension2.OwnerLabel.isEnabled())
        # self.assertFalse(_IncomeInfoTab.pension2.Owner.isEnabled())

        _InputsTab.tabs.setCurrentIndex(5)  # select Global tab
        self.assertFalse(_GlobalVariablesTab._FilingStatusOnceWidowed.isEnabled())

        # change status to Married...
        # _status.setCurrentText(RelationStatusType.Married.name)
        _status.set(RelationStatusType.MARRIED)
        self.assertEqual(_status.get(), RelationStatusType.MARRIED)

        # make sure that spouse widgets are enabled since We choose married
        _InputsTab.tabs.setCurrentIndex(0)  # select Basic Tab
        self.assertTrue(_BasicInfoTab._spouseinfo.isEnabled())

        _InputsTab.tabs.setCurrentIndex(3)  # select Asset
        self.assertTrue(_AssetInfoTab._spouseinfo.isEnabled())

        _InputsTab.tabs.setCurrentIndex(1)  # select Income Tab..
        self.assertTrue(_IncomeInfoTab.spouseSS.isEnabled())
        # self.assertTrue(_IncomeInfoTab.pension1OwnerLabel.isEnabled())
        self.assertTrue(_IncomeInfoTab.pension1.Owner.isEnabled())
        # self.assertTrue(_IncomeInfoTab.pension2OwnerLabel.isEnabled())
        self.assertTrue(_IncomeInfoTab.pension2.Owner.isEnabled())

        _InputsTab.tabs.setCurrentIndex(5)  # select Global tab
        self.assertTrue(_GlobalVariablesTab._FilingStatusOnceWidowed.isEnabled())


if __name__ == "__main__":
    unittest.main()
