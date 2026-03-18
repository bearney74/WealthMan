import unittest
from datetime import date

from src.libs.Person import Person
from src.libs.RequiredMinimalDistributions import RMDTable, RMDCalcs

from src.libs.EnumTypes import AccountOwnerType
from src.libs.Account import TraditionalIRA
from src.libs.SurplusAccount import SurplusAccount

# FRA means Full Retirement Age


class RMDTest(unittest.TestCase):
    def test_single(self):
        _p = Person(name="Jane", birthDate=date(1960, 1, 1))
        _rmd = RMDTable(_p, None)

        # before age 73 (30 years of age)
        self.assertEqual(_rmd.calcPercent(date(1990, 1, 1)), 0.0)

        # just before 73 birthday
        self.assertEqual(_rmd.calcPercent(date(2032, 12, 31)), 0.0)

        # on 73 birthday
        self.assertEqual(_rmd.calcPercent(date(2033, 1, 1)), 100.0 / 26.5)

        # on 80 birthday
        self.assertEqual(_rmd.calcPercent(date(2040, 1, 1)), 100.0 / 20.2)

        # 100
        self.assertEqual(_rmd.calcPercent(date(2060, 1, 1)), 100.0 / 6.4)

        # 120 and over are the same
        self.assertEqual(_rmd.calcPercent(date(2080, 1, 1)), 100.0 / 2.0)

        # 125
        self.assertEqual(_rmd.calcPercent(date(2085, 1, 1)), 100.0 / 2.0)


class RMDCalcsTest(unittest.TestCase):
    def test_RMDCalcs(self):
        _ira = TraditionalIRA(
            Name="Client Trad IRA",
            Owner=AccountOwnerType.CLIENT,
            Balance=1000,
            InterestRate=0.0,
        )
        _surplus = SurplusAccount(0, 0.0)

        _ira.beginning_of_year_bookkeeping()
        _surplus.beginning_of_year_bookkeeping()

        _rmdcalcs = RMDCalcs(_ira, _surplus)
        _withdraw_amount, _, _ = _rmdcalcs.calcRequiredAmount(
            5.0
        )  # 5.0 % of balance needs to be withdrawn this year..
        self.assertEqual(_withdraw_amount, 50)
        _rmdcalcs.do_transfer_if_necessary()

        self.assertEqual(_ira.totalWithdraws, 50)
        self.assertEqual(_surplus.totalDeposits, 50)


if __name__ == "__main__":
    unittest.main()
