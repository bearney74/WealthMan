import unittest
from datetime import date

from src.libs.TransferAsset import TransferAssets
from src.libs.Account import TraditionalIRA, RothIRA, Brokerage
from src.libs.EnumTypes import AccountOwnerType
from src.libs.Person import Person


class TransferAssetTest(unittest.TestCase):
    def test_TransferAssetsIRA2Roth(self):
        _src = TraditionalIRA(
            Name="Trad IRA",
            Owner=AccountOwnerType.CLIENT,
            Balance=1000,
            InterestRate=1.0,
        )

        _tgt = RothIRA(
            Name="Roth IRA",
            Owner=AccountOwnerType.CLIENT,
            Balance=500,
            InterestRate=2.0,
        )

        _person = Person("John Doe", birthDate=date(1990, 1, 1))

        _trans = TransferAssets("my transfer", _src, _tgt, 100, 0.0, _person, 30, 40)
        _trans.do_transfer(year=2020)

        self.assertEqual(_trans.taxable_income, 100)
        self.assertEqual(_trans.ltcg_income, 0)

    def test_TransferAssetsIRA2Brokerage(self):
        _src = TraditionalIRA(
            Name="Trad IRA",
            Owner=AccountOwnerType.CLIENT,
            Balance=1000,
            InterestRate=1.0,
        )

        _tgt = Brokerage(
            Name="Roth IRA",
            Owner=AccountOwnerType.CLIENT,
            Balance=500,
            InterestRate=2.0,
        )

        _person = Person("John Doe", birthDate=date(1990, 1, 1))

        _trans = TransferAssets("my transfer", _src, _tgt, 100, 0.0, _person, 30, 40)
        _trans.do_transfer(year=2020)

        self.assertEqual(_trans.taxable_income, 100)
        self.assertEqual(_trans.ltcg_income, 0)

    def test_TransferAssetsRoth2Brokerage(self):
        _src = RothIRA(
            Name="Trad IRA",
            Owner=AccountOwnerType.CLIENT,
            Balance=1000,
            InterestRate=1.0,
        )

        _tgt = Brokerage(
            Name="Roth IRA",
            Owner=AccountOwnerType.CLIENT,
            Balance=500,
            InterestRate=2.0,
        )

        _person = Person("John Doe", birthDate=date(1990, 1, 1))

        _trans = TransferAssets("my transfer", _src, _tgt, 100, 0.0, _person, 30, 40)
        _trans.do_transfer(year=2020)

        self.assertEqual(_trans.taxable_income, 0)
        self.assertEqual(_trans.ltcg_income, 0)

    def test_TransferAssetsBrokerage2Brokerage(self):
        _src = Brokerage(
            Name="Brokerage",
            Owner=AccountOwnerType.CLIENT,
            Balance=1000,
            InterestRate=1.0,
        )

        _tgt = Brokerage(
            Name="Cash",
            Owner=AccountOwnerType.CLIENT,
            Balance=500,
            InterestRate=2.0,
        )

        _person = Person("John Doe", birthDate=date(1990, 1, 1))

        _trans = TransferAssets("my transfer", _src, _tgt, 100, 0.0, _person, 30, 40)
        _trans.do_transfer(year=2020)

        self.assertEqual(_trans.taxable_income, 0)  # is this correct?
        self.assertEqual(_trans.ltcg_income, 100)


if __name__ == "__main__":
    unittest.main()
