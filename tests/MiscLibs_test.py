import unittest

from src.libs.MiscLibs import PeriodValidator


class MiscLibsTest(unittest.TestCase):
    def test_PeriodValidator(self):
        _p = PeriodValidator(birthYear=2000, beginAge=20, endAge=25)

        for _year in range(2010, 2020):
            self.assertFalse(_p.isa_valid_period(_year))

        for _year in range(2020, 2026):
            self.assertTrue(_p.isa_valid_period(_year))

        for _year in range(2026, 2030):
            self.assertFalse(_p.isa_valid_period(_year))

        # try before the person is alive
        self.assertFalse(_p.isa_valid_period(1999))


if __name__ == "__main__":
    unittest.main()
