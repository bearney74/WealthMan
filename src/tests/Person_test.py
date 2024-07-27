import unittest
from datetime import date

from libs.Person import Person


class PersonTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_calc_date_by_age(self):
        _p = Person("Sam", birthDate=date(2000, 1, 1), retirementAge=65, lifeSpanAge=80)
        self.assertEqual(_p.calc_date_by_age(20), date(2020, 1, 1))

        self.assertEqual(_p.calc_date_by_age(50), date(2050, 1, 1))

    def test_calc_age_by_date(self):
        _p = Person("Sam", birthDate=date(2000, 2, 1), retirementAge=65, lifeSpanAge=80)
        self.assertEqual(_p.calc_age_by_date(date(2035, 2, 3)), 35)
        self.assertEqual(_p.calc_age_by_date(date(2035, 1, 31)), 34)

        self.assertEqual(_p.calc_age_by_date(date(2065, 10, 31)), 65)

    def test_calc_age_by_year(self):
        _p = Person("Sam", birthDate=date(2000, 2, 1), retirementAge=65, lifeSpanAge=80)
        self.assertEqual(_p.calc_age_by_year(2010), 10)
        self.assertEqual(_p.calc_age_by_year(2035), 35)
        self.assertEqual(_p.calc_age_by_year(2070), 70)


if __name__ == "__main__":
    unittest.main()
