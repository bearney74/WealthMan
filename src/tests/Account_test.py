import unittest
from datetime import date

from libs.Account import Account, TraditionalIRA, RothIRA, Brokerage
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

    def test_AccountInterestRate(self):
        _a = Account(
            "Cola", AccountType.Regular, AccountOwnerType.Client, InterestRate=0.1
        )
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
            InterestRate=0.1,
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


class TraditionalIRATest(unittest.TestCase):
    def test_basic(self):
        _a = TraditionalIRA(
            "basic",
            Owner=AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            Balance=1000.0,
        )
        _a.deposit(500)
        _a.withdraw(300)
        self.assertEqual(_a.Balance, 200)
        self.assertEqual(_a.taxable_income, 300)
        self.assertEqual(_a.ltcg_income, 0)


class RothIRATest(unittest.TestCase):
    def test_basic(self):
        _a = RothIRA(
            "basic",
            Owner=AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            Balance=1000.0,
        )
        _a.deposit(500)
        _a.withdraw(300)
        self.assertEqual(_a.Balance, 200)
        self.assertEqual(_a.taxable_income, 0)
        self.assertEqual(_a.ltcg_income, 0)


class BrokerageTest(unittest.TestCase):
    def test_basic(self):
        _a = Brokerage(
            "basic",
            Owner=AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            Balance=1000.0,
        )
        _a.deposit(500)
        _a.withdraw(300)
        self.assertEqual(_a.Balance, 200)
        self.assertEqual(_a.taxable_income, 0)
        self.assertEqual(
            _a.ltcg_income, 300
        )  # 300 probably isn't right for LTCG, but will have
        # to work for now.


if __name__ == "__main__":
    unittest.main()
