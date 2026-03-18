import unittest

from src.libs.IncomeSources import IncomeSource
from src.libs.EnumTypes import IncomeSourceType, PersonType
from src.libs.MiscLibs import PeriodValidator


class IncomeSourceTest(unittest.TestCase):
    def test_Employment(self):
        _p = PeriodValidator(birthYear=2000, beginAge=20, endAge=30)
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.EMPLOYMENT,
            Amount=100_000,
            Owner=PersonType.CLIENT,
            Period=_p,
            COLA=1.0,
        )

        self.assertEqual(0, _is.calc_income_by_year(2019))  # is zero since person is 19

        _balance = 100_000
        for _year in range(2020, 2030):
            _bal = _is.calc_income_by_year(_year)
            self.assertEqual(_bal, _balance)
            _balance = int(_balance * 1.01)

        self.assertEqual(0, _is.calc_income_by_year(2031))  # is zero since person is 31

    # add back in sometime
    """
    
    def test_SurvivorBenefit100(self):
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.PENSION,
            Amount=50_000,
            Owner=PersonType.CLIENT,
            BirthDate=date(2000, 1, 1),
            SurvivorPercent=100.0,
            COLA=0.0,
        )

        _balance = 50_000
        for _year in range(2020, 2030):
            _balance = _is.calc_balance_by_year(_year)
            self.assertEqual(_balance, 50_000)

    def test_SurvivorBenefit50(self):
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.PENSION,
            Amount=50_000,
            Owner=PersonType.CLIENT,
            #BirthDate=date(2000, 1, 1),
            LifeSpanAge=20,
            SurvivorPercent=50.0,
            COLA=0.0,
        )

        for _year in range(2025, 2030):
            _balance = _is.calc_balance_by_year(_year)
            self.assertEqual(_balance, 25_000)

    def test_SurvivorBenefit0(self):
        _is = IncomeSource(
            "test",
            IncomeType=IncomeSourceType.PENSION,
            Amount=50_000,
            Owner=PersonType.CLIENT,
            BirthDate=date(2000, 1, 1),
            LifeSpanAge=20,
            SurvivorPercent=0.0,
            COLA=0.0,
        )

        for _year in range(2025, 2030):
            _balance = _is.calc_balance_by_year(_year)
            self.assertEqual(_balance, 0)
    """


if __name__ == "__main__":
    unittest.main()
