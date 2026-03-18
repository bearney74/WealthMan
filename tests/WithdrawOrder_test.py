import unittest

from src.libs.WithdrawStrategy import WithdrawStrategy, WithdrawOrderType2List
from src.libs.Account import TraditionalIRA, RothIRA, Brokerage
from src.libs.EnumTypes import AccountType, AccountOwnerType, WithdrawOrderType


class WithdrawOrderTest(unittest.TestCase):
    def test_WithdrawOrderType2List(self):
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TAXDEFERRED_REGULAR_TAXFREE),
            [AccountType.TAXDEFERRED, AccountType.REGULAR, AccountType.TAXFREE],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TAXDEFERRED_TAXFREE_REGULAR),
            [AccountType.TAXDEFERRED, AccountType.TAXFREE, AccountType.REGULAR],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.REGULAR_TAXFREE_TAXDEFERRED),
            [AccountType.REGULAR, AccountType.TAXFREE, AccountType.TAXDEFERRED],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.REGULAR_TAXDEFERRED_TAXFREE),
            [AccountType.REGULAR, AccountType.TAXDEFERRED, AccountType.TAXFREE],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TAXFREE_TAXDEFERRED_REGULAR),
            [AccountType.TAXFREE, AccountType.TAXDEFERRED, AccountType.REGULAR],
        )
        self.assertEqual(
            WithdrawOrderType2List(WithdrawOrderType.TAXFREE_REGULAR_TAXDEFERRED),
            [AccountType.TAXFREE, AccountType.REGULAR, AccountType.TAXDEFERRED],
        )

    def test_TAXDEFERRED_REGULAR_TAXFREE(self):
        # tax deferred
        _trad = TraditionalIRA(
            Name="Trad IRA",
            Owner=AccountOwnerType.CLIENT,
            # BirthDate=date(1990, 1, 1),
            Balance=1000,
            InterestRate=1.0,
        )

        # tax free
        _roth = RothIRA(
            Name="Roth IRA",
            Owner=AccountOwnerType.CLIENT,
            # BirthDate=date(1990, 1, 1),
            Balance=500,
            InterestRate=2.0,
        )

        # REGULAR
        _brokerage = Brokerage(
            Name="Brokerage",
            Owner=AccountOwnerType.CLIENT,
            # BirthDate=date(1990, 1, 1),
            Balance=500,
            InterestRate=2.0,
        )

        _ws = WithdrawStrategy(
            WithdrawOrderType.TAXDEFERRED_REGULAR_TAXFREE,
            60,
            True,
            60,
            False,
            [_trad, _roth, _brokerage],
        )
        _deficit, _dict = _ws.reconcile_required_withdraw(100)

        self.assertEqual(_deficit, 0)
        self.assertEqual(_dict[AccountType.TAXDEFERRED], 100)
        self.assertEqual(_dict[AccountType.TAXFREE], 0)
        self.assertEqual(_dict[AccountType.REGULAR], 0)
        self.assertEqual(_trad.balance, 900)
        self.assertEqual(_roth.balance, 500)
        self.assertEqual(_brokerage.balance, 500)

    def test_insufficient_funds(self):
        # tax deferred
        _trad = TraditionalIRA(
            Name="Trad IRA",
            Owner=AccountOwnerType.CLIENT,
            # BirthDate=date(1990, 1, 1),
            Balance=1000,
            InterestRate=1.0,
        )

        _roth = RothIRA(
            Name="Roth IRA",
            Owner=AccountOwnerType.SPOUSE,
            # BirthDate=date(1990, 1, 1),
            Balance=0,
            InterestRate=2.0,
        )

        _ws = WithdrawStrategy(
            WithdrawOrderType.TAXDEFERRED_REGULAR_TAXFREE,
            60,
            True,
            60,
            False,
            [_trad, _roth],
        )

        _deficit, _dict = _ws.reconcile_required_withdraw(5_000)

        self.assertEqual(_deficit, 4000)
        self.assertEqual(_dict[AccountType.TAXDEFERRED], 1000)
        self.assertEqual(_dict[AccountType.TAXFREE], 0)
        self.assertEqual(_dict[AccountType.REGULAR], 0)
        self.assertEqual(_trad.balance, 0)
        self.assertEqual(_roth.balance, 0)


if __name__ == "__main__":
    unittest.main()
