import unittest

from src.libs.MiscLibs import PeriodValidator
from src.libs.Expense import Expense


class ExpensesTest(unittest.TestCase):
    def test_Expenses(self):
        _p = PeriodValidator(birthYear=2000, beginAge=20, endAge=25)

        _e = Expense("Expense Test", 1000, Period=_p)

        for _year in range(2010, 2020):
            self.assertEqual(0, _e.calc_balance_by_year(_year))  # 0% inflation

        for _year in range(2020, 2026):
            self.assertEqual(1000, _e.calc_balance_by_year(_year))  # 0% inflation

        for _year in range(2026, 2030):
            self.assertEqual(0, _e.calc_balance_by_year(_year))  # 0% inflation

    def test_InflationCOLA(self):
        def cola_inflation(cola, inflation):
            _p = PeriodValidator(birthYear=2000, beginAge=20, endAge=25)

            _e = Expense("Expense Test", 1000, Period=_p, COLA=cola)

            for _year in range(2010, 2020):
                self.assertEqual(0, _e.calc_balance_by_year(_year, inflation))

            _value = 1000
            for _year in range(2020, 2026):
                self.assertEqual(
                    _value, _e.calc_balance_by_year(_year, inflation)
                )  # 0% inflation
                _value = int(_value * (1.0 + (cola - inflation) / 100.0))

            for _year in range(2026, 2030):
                self.assertEqual(
                    0, _e.calc_balance_by_year(_year, inflation)
                )  # 0% inflation

        cola_inflation(0.0, 0.0)
        cola_inflation(10.0, 0.0)
        cola_inflation(0.0, 10.0)
        cola_inflation(10.0, 10.0)

    def test_COLA_flag(self):
        _e = Expense("Expense Test", 1000)
        self.assertFalse(_e.get_COLA_Flag())

        _e = Expense("Expense Test", 1000, COLA=None)
        self.assertFalse(_e.get_COLA_Flag())

        _e = Expense("Expense Test", 1000, COLA=0.0)
        self.assertFalse(_e.get_COLA_Flag())

        # now COLA FLAG should be True  (non None.. non zero value for COLA)
        _e = Expense("Expense Test", 1000, COLA=1.0)
        self.assertTrue(_e.get_COLA_Flag())


if __name__ == "__main__":
    unittest.main()
