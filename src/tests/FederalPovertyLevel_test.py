import unittest

from libs.FederalPovertyLevel import FederalPovertyLevel


class DateHelperTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_FPL(self):
        _fpl = FederalPovertyLevel(1)
        _fpl.calc_percent(10_000)
        self.assertEqual(
            _fpl.calc_percent(10_000), int(100.0 * 10_000 / _fpl.FPL_100Percent)
        )

        _fpl.calc_percent(50_000)
        self.assertEqual(
            _fpl.calc_percent(50_000), int(100.0 * 50_000 / _fpl.FPL_100Percent)
        )

        _fpl = FederalPovertyLevel(2)
        _fpl.calc_percent(10_000)
        self.assertEqual(
            _fpl.calc_percent(10_000), int(100.0 * 10_000 / _fpl.FPL_100Percent)
        )

        _fpl.calc_percent(50_000)
        self.assertEqual(
            _fpl.calc_percent(50_000), int(100.0 * 50_000 / _fpl.FPL_100Percent)
        )


if __name__ == "__main__":
    unittest.main()
