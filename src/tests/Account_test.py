import unittest
from datetime import date

from libs.Account import Account
from libs.EnumTypes import AccountType, AccountOwnerType


class AccountTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_basicAccount(self):
        _a = Account("basic", AccountType.Regular, AccountOwnerType.Client)
        _a.deposit(500)
        self.assertEqual(_a.Balance, 500)

        _a.withdraw(400)
        self.assertEqual(_a.Balance, 100)

        _a.calc_balance()  # no year set.. no Contribution set, Cola=0 etc..  should return unmodified balance
        self.assertEqual(_a.Balance, 100)

    def test_AccountCOLA(self):
        _a = Account("Cola", AccountType.Regular, AccountOwnerType.Client, COLA=0.1)
        _a.deposit(500)
        self.assertEqual(_a.Balance, 500)

        _a.calc_balance()
        self.assertEqual(_a.Balance, 550)

    def test_AccountContribution(self):
        _a = Account(
            "Contribution",
            AccountType.Regular,
            AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            Contribution=1000,
        )

        _a.calc_balance(year=2010)  # anything over 2000 should work..
        self.assertEqual(_a.Balance, 1000)

    def test_AccountContribution1(self):
        _a = Account(
            "Contribution",
            AccountType.Regular,
            AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            Contribution=1000,
            ContributionBeginAge=20,
            ContributionEndAge=30,
            COLA=0.1,
        )

        # balance is 0

        # we don't add a contribution before 2020, so this should be zero
        for _year in range(2000, 2020):
            _a.calc_balance(year=_year)
            self.assertEqual(_a.Balance, 0)

        _total = 0
        for _year in range(2020, 2030):
            _a.calc_balance(year=_year)  # anything over 2000 should work..
            _total = int(_total * 1.1)
            _total += 1000
            self.assertEqual(_a.Balance, _total)


if __name__ == "__main__":
    unittest.main()
