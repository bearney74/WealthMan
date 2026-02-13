import unittest
from datetime import date

from libs.IncomeSources import IncomeSource
from libs.EnumTypes import IncomeSourceType, AmountPeriodType, AccountOwnerType


class IncomeSourceTest(unittest.TestCase):
    def test_Employment(self):
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.Employment,
            Amount=100_000,
            AmountPeriod=AmountPeriodType.Annual,
            Owner=AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            COLA=1.0,
        )

        _balance = 100_000
        for _year in range(2020, 2030):
            _bal = _is.calc_balance_by_year(_year)
            self.assertEqual(_bal, _balance)
            _balance = int(_balance * 1.01)

    def test_SurvivorBenefit100(self):
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.Pension,
            Amount=50_000,
            AmountPeriod=AmountPeriodType.Annual,
            Owner=AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            SurvivorPercent=100.0,
            COLA=0.0,
        )

        _balance = 50_000
        for _year in range(2020, 2030):
            _balance = _is.calc_balance_by_year(_year)
            self.assertEqual(_balance, 50_000)
            # _balance=int(_balance * 1.01)

    def test_SurvivorBenefit50(self):
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.Pension,
            Amount=50_000,
            AmountPeriod=AmountPeriodType.Annual,
            Owner=AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            LifeSpanAge=20,
            SurvivorPercent=50.0,
            COLA=0.0,
        )

        for _year in range(2025, 2030):
            _balance = _is.calc_balance_by_year(_year)
            self.assertEqual(_balance, 25_000)
            # _balance=int(_balance * 1.01)

    def test_SurvivorBenefit0(self):
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.Pension,
            Amount=50_000,
            AmountPeriod=AmountPeriodType.Annual,
            Owner=AccountOwnerType.Client,
            BirthDate=date(2000, 1, 1),
            LifeSpanAge=20,
            SurvivorPercent=0.0,
            COLA=0.0,
        )

        for _year in range(2025, 2030):
            _balance = _is.calc_balance_by_year(_year)
            self.assertEqual(_balance, 0)
            # _balance=int(_balance * 1.01)


if __name__ == "__main__":
    unittest.main()
