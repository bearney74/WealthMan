import unittest
from datetime import date

from src.libs.WithdrawStrategy import WithdrawStrategy, WithdrawOrderType2List
from src.libs.Account import TraditionalIRA, RothIRA, Brokerage
from src.libs.EnumTypes import AccountType, AccountOwnerType, WithdrawOrderType


class WithdrawOrderTest(unittest.TestCase):
    def test_WithdrawOrderType2List(self):
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TaxDeferred_Regular_TaxFree),
            [AccountType.TaxDeferred, AccountType.Regular, AccountType.TaxFree],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TaxDeferred_TaxFree_Regular),
            [AccountType.TaxDeferred, AccountType.TaxFree, AccountType.Regular],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.Regular_TaxFree_TaxDeferred),
            [AccountType.Regular, AccountType.TaxFree, AccountType.TaxDeferred],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.Regular_TaxDeferred_TaxFree),
            [AccountType.Regular, AccountType.TaxDeferred, AccountType.TaxFree],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TaxFree_TaxDeferred_Regular),
            [AccountType.TaxFree, AccountType.TaxDeferred, AccountType.Regular],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TaxFree_Regular_TaxDeferred),
            [AccountType.TaxFree, AccountType.Regular, AccountType.TaxDeferred],
        )

    def test_TaxDeferred_Regular_TaxFree(self):
        # tax deferred
        _trad = TraditionalIRA(
            Name="Trad IRA",
            Owner=AccountOwnerType.Client,
            BirthDate=date(1990, 1, 1),
            Balance=1000,
            InterestRate=1.0,
        )

        # tax free
        _roth = RothIRA(
            Name="Roth IRA",
            Owner=AccountOwnerType.Client,
            BirthDate=date(1990, 1, 1),
            Balance=500,
            InterestRate=2.0,
        )

        # Regular
        _brokerage = Brokerage(
            Name="Brokerage",
            Owner=AccountOwnerType.Client,
            BirthDate=date(1990, 1, 1),
            Balance=500,
            InterestRate=2.0,
        )

        _ws = WithdrawStrategy(
            WithdrawOrderType.TaxDeferred_Regular_TaxFree,
            60,
            True,
            60,
            False,
            [_trad, _roth, _brokerage],
        )
        _deficit, _dict = _ws.reconcile_required_withdraw(100)

        self.assertEqual(_deficit, 0)
        self.assertEqual(_dict[AccountType.TaxDeferred], 100)
        self.assertEqual(_dict[AccountType.TaxFree], 0)
        self.assertEqual(_dict[AccountType.Regular], 0)
        self.assertEqual(_trad.Balance, 900)
        self.assertEqual(_roth.Balance, 500)
        self.assertEqual(_brokerage.Balance, 500)

    def test_insufficient_funds(self):
        # tax deferred
        _trad = TraditionalIRA(
            Name="Trad IRA",
            Owner=AccountOwnerType.Client,
            BirthDate=date(1990, 1, 1),
            Balance=1000,
            InterestRate=1.0,
        )

        _ws = WithdrawStrategy(
            WithdrawOrderType.TaxDeferred_Regular_TaxFree,
            60,
            True,
            60,
            False,
            [_trad],
        )

        _deficit, _dict = _ws.reconcile_required_withdraw(5_000)

        self.assertEqual(_deficit, 4000)
        self.assertEqual(_dict[AccountType.TaxDeferred], 1000)
        self.assertEqual(_dict[AccountType.TaxFree], 0)
        self.assertEqual(_dict[AccountType.Regular], 0)
        self.assertEqual(_trad.Balance, 0)


if __name__ == "__main__":
    unittest.main()
