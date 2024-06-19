import unittest
from datetime import date

import sys

sys.path.append("../src")
from libs.Person import Person
from libs.RequiredMinimalDistributions import RMD

# FRA means Full Retirement Age


class RMDTest(unittest.TestCase):
    """tests to verify that early/late SS payment calcs are correct"""

    def test_single(self):
        _p = Person(Name="Jane", BirthDate=date(1960, 1, 1))
        _rmd = RMD(_p, None)

        # before age 73 (30 years of age)
        self.assertEqual(_rmd.calc(date(1990, 1, 1)), 0.0)

        # just before 73 birthday
        self.assertEqual(_rmd.calc(date(2032, 12, 31)), 0.0)

        # on 73 birthday
        self.assertEqual(_rmd.calc(date(2033, 1, 1)), 100.0 / 26.5)

        # on 80 birthday
        self.assertEqual(_rmd.calc(date(2040, 1, 1)), 100.0 / 20.2)

        # 100
        self.assertEqual(_rmd.calc(date(2060, 1, 1)), 100.0 / 6.4)

        # 120 and over are the same
        self.assertEqual(_rmd.calc(date(2080, 1, 1)), 100.0 / 2.0)

        # 125
        self.assertEqual(_rmd.calc(date(2085, 1, 1)), 100.0 / 2.0)


if __name__ == "__main__":
    unittest.main()
