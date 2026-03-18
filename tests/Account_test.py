import unittest

from src.libs.Account import (
    Account,
    TraditionalIRA,
    RothIRA,
    Brokerage,
    ContributionClass,
)
from src.libs.EnumTypes import AccountType, AccountOwnerType


class AccountTest(unittest.TestCase):
    def test_basicAccount(self):
        _a = Account("basic", AccountType.REGULAR, AccountOwnerType.CLIENT)
        _a.deposit(500)
        self.assertEqual(_a.balance, 500)

        _a.withdraw(400)
        self.assertEqual(_a.balance, 100)

        self.assertEqual(
            0, _a.calc_interest()
        )  # no year set.. no Contribution set, Cola=0 etc..  should return unmodified balance
        self.assertEqual(_a.balance, 100)

    def test_AccountInterestRate(self):
        _a = Account(
            "Cola", AccountType.REGULAR, AccountOwnerType.CLIENT, InterestRate=10.0
        )
        _a.deposit(500)
        self.assertEqual(_a.balance, 500)

        self.assertEqual(50, _a.calc_interest())

        self.assertEqual(
            _a.balance, 500
        )  # should still be 500 since we have not done bookkeeping

        _a.end_of_year_bookkeeping()
        self.assertEqual(_a.balance, 550)

    def test_AccountContribution(self):
        _con = ContributionClass(1000, birthYear=2000, beginAge=10, endAge=None)
        _a = Account(
            "Contribution",
            AccountType.REGULAR,
            AccountOwnerType.CLIENT,
            ContributionObj=_con,
        )

        self.assertEqual(
            1000, _a.do_contribution(year=2010, number_of_years=0, inflation=0.0)
        )  # anything over 2000 should work..
        self.assertEqual(_a.contributions, 1000)

    def test_AccountContribution1(self):
        _con = ContributionClass(1000, birthYear=2000, beginAge=20, endAge=30)
        _a = Account(
            "Contribution",
            AccountType.REGULAR,
            AccountOwnerType.CLIENT,
            InterestRate=10.0,
            ContributionObj=_con,
        )

        # balance is 0

        # we don't add a contribution before 2020, so this should be zero
        for _year in range(2000, 2020):
            self.assertEqual(
                0,
                _a.do_contribution(
                    year=_year, number_of_years=_year - 2000, inflation=0.0
                ),
            )
            self.assertEqual(_a.contributions, 0)

        for _year in range(2020, 2030):
            _a.beginning_of_year_bookkeeping()
            self.assertEqual(
                1000,
                _a.do_contribution(
                    year=_year, number_of_years=_year - 2000, inflation=0.0
                ),
            )  # anything over 2000 should work..
            self.assertEqual(1000, _a.contributions, "Year=%s" % _year)

    def test_AccountContribution2(self):
        _con = ContributionClass(1000, birthYear=2000, beginAge=20, endAge=30)
        _a = Account(
            "Contribution",
            AccountType.REGULAR,
            AccountOwnerType.CLIENT,
            InterestRate=10.0,
            ContributionObj=_con,
        )

        _total = 0
        for _year in range(2020, 2030):
            self.assertEqual(_a.balance, _total, "Year=%s" % _year)
            _a.beginning_of_year_bookkeeping()
            _a.do_contribution(year=_year, number_of_years=_year - 2020, inflation=0.0)
            _total += 1000  # add contribution first
            _total = int(
                _total * 1.1
            )  # then calc balance (which includes the contribution)
            _a.calc_interest()
            _a.end_of_year_bookkeeping()  # this is the only way to adjust the balance..
            self.assertEqual(_a.balance, _total, "Year=%s" % _year)


class TraditionalIRATest(unittest.TestCase):
    def test_basic(self):
        _a = TraditionalIRA(
            "basic",
            Owner=AccountOwnerType.CLIENT,
            Balance=1000,
        )
        _a.deposit(500)
        _a.withdraw(300)
        self.assertEqual(_a.balance, 1200)
        self.assertEqual(_a.taxable_income, 300)
        self.assertEqual(_a.ltcg_income, 0)


class RothIRATest(unittest.TestCase):
    def test_basic(self):
        _a = RothIRA(
            "basic",
            Owner=AccountOwnerType.CLIENT,
            # BirthDate=date(2000, 1, 1),
            Balance=1000,
        )
        _a.deposit(500)
        _a.withdraw(300)
        self.assertEqual(_a.balance, 1200)
        self.assertEqual(_a.taxable_income, 0)
        self.assertEqual(_a.ltcg_income, 0)


class BrokerageTest(unittest.TestCase):
    def test_basic(self):
        _a = Brokerage(
            "basic",
            Owner=AccountOwnerType.CLIENT,
            Balance=1000,
        )
        _a.deposit(500)
        _a.withdraw(300)
        self.assertEqual(_a.balance, 1200)
        self.assertEqual(_a.taxable_income, 0)
        self.assertEqual(
            _a.ltcg_income, 300
        )  # 300 probably isn't right for LTCG, but will have
        # to work for now.


if __name__ == "__main__":
    unittest.main()
